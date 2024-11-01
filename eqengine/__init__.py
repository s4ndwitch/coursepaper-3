
from rsa import PublicKey, verify
from threading import Thread

from serialiser import Serialiser
from serialiser.user import User
from serialiser.post import Post
from eqengine.peer import Peer

class EqEngine:
    
    _serialiser: Serialiser
    _peer: Peer
    _peer_thread: Thread
    
    def __init__(self, uid: str, address: str, port: int, db_file: str = "db.sqlite", peer_file: str = "peer.ini") -> None:
        
        self._serialiser = Serialiser(db_file=db_file)

        self._peer = Peer(self, uid=uid, address=address, port=port, table_file=peer_file)
        self._peer_thread = Thread(target=self._peer.run)
        self._peer_thread.start()
    
    def hello(self, address: str, port: int):
        self._peer.hello(host=address, port=port)

    def shutdown(self) -> None:
        
        self._peer.shutdown_flag = True
        self._peer_thread.join()
    
    def _verify(self, text: str, signature: str, pubkey: str) -> bool:
        
        pub_key: PublicKey = PublicKey.load_pkcs1(pubkey)
        
        signature = bytes().fromhex(signature)
        
        return verify(
            message=text.encode(),
            signature=signature,
            pub_key=pub_key
        )
    
    def handleData(self, data: list, debug: bool = False) -> None:
        
        for element in data:
            if element["type"] == "user":
                
                if ("uid" not in element.keys()):
                    continue
                
                if self._serialiser.getUser(element["uid"]) == None:
                    
                    if ("nickname" not in element.keys() or \
                        "pubkey" not in element.keys()):
                        continue
                    
                    self._serialiser.createUser(
                        uid=element["uid"],
                        nickname=element["nickname"],
                        pubkey=element["pubkey"]
                    )
        
        for element in data:
            if element["type"] == "post":
                
                if (set([
                    "uid", "author", "text", "signature", "type"
                ]) != set(element.keys())):
                    continue
                
                if self._serialiser.getPost(element["uid"]) == None:
                    
                    author = self._serialiser.getUser(element["author"])
                    
                    if author == None:
                        continue
                    
                    pubkey = author.pubkey
                    
                    if debug or self._verify(
                        text=element["text"],
                        signature=element["signature"],
                        pubkey=pubkey
                    ):

                        self._serialiser.createPost(
                            uid=element["uid"],
                            author=element["author"],
                            text=element["text"],
                            signature=element["signature"]
                        )
    
    def request(self, data: list, online=False) -> list:
        
        for element in data:
            
            if element["type"] == "user":
                
                if not online:
                    result: list = self._peer.request(element["uid"])
                    result = result[0]["posts"]
                    for post in result:
                        self._peer.request(post, peer_uid=element["uid"], request_type="post")
                
                user: User = self._serialiser.getUser(element["uid"])
                posts: list = self._serialiser.getPosts(element["uid"])
                
                if user is not None:
                    element["pubkey"] = user.pubkey
                    element["nickname"] = user.nickname
                    element["posts"] = posts
            
            if element["type"] == "post":
                
                post: Post = self._serialiser.getPost(element["uid"])
                
                if post is not None:
                    element["text"] = post.text
                    element["signature"] = post.signature
                    element["author"] = post.author
        
        return data
