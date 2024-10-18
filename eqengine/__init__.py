
from rsa import PublicKey, verify

from serialiser import Serialiser

class EqEngine:
    
    _serialiser: Serialiser
    
    def __init__(self, db_file="db.sqlite") -> None:
        
        self._serialiser = Serialiser(db_file=db_file)
    
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
        pass
