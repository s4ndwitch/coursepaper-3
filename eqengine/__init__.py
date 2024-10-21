
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
    
    def __init__(self, db_file="db.sqlite") -> None:
        
        self._serialiser = Serialiser(db_file=db_file)

        self._peer = Peer(self)
        self._peer_thread = Thread(target=self._peer.run)
        self._peer_thread.start()
    
    def shutdown(self) -> None:
        
        self._peer.shutdown_flag = True
        self._peer_thread.join()
    
    def _verify(self, author: str, text: str, signature: str, pubkey: str) -> bool:
        
        pub_key: PublicKey = PublicKey.load_pkcs1(pubkey)
        
        return verify(
            message=(author + text),
            signature=signature,
            pub_key=pub_key
        )
    
    def handleData(self, data: list) -> None:
        
        for element in data:
            if element["type"] == "user":
                
                if (set([
                    "uid", "nickname", "pubkey", "type"
                ]) != set(element.keys())):
                    continue
                
                if self._serialiser.getUser(element["uid"]) == None:
                    
                    self._serialiser.createUser(
                        uid=element["uid"],
                        nickname=element["nickname"],
                        pubkey=element["pubkey"]
                    )
            
            elif element["type"] == "post":
                
                if (set([
                    "uid", "author", "text", "signature", "pubkey"
                ]) != set(element.keys())):
                    continue
                
                if self._serialiser.getPost(element["uid"]) == None:
                    if self._verify(
                        author=element["author"],
                        text=element["text"],
                        signature=element["signature"],
                        pubkey=element["pubkey"]
                    ):

                        self._serialiser.createPost(
                            author=element["author"],
                            text=element["text"],
                            signature=element["signature"],
                            pubkey=element["pubkey"]
                        )
    
    def request(self, data: list) -> list:
        
        for element in data:
            
            if element["type"] == "user":
                
                user: User = self._serialiser.getUser(element["uid"])
                
                if user is not None:
                    element["pubkey"] = user.pubkey
                    element["nickname"] = user.nickname
            
            if element["type"] == "post":
                
                post: Post = self._serialiser.getPost(element["uid"])
                
                if post is not None:
                    element["text"] = post.text
                    element["signature"] = post.signature
                    element["author"] = post.author
        
        return data
