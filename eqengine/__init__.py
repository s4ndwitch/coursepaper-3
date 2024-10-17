
from rsa import PublicKey, verify

class EqEngine:
    
    def __init__(self) -> None:
        pass
    
    def _verify(self, hash: bytes, signature: bytes, pubkey: PublicKey) -> bool:
        
        return hash == verify(signature, pubkey)
    
    def handleData(self, data: dict) -> None:
        pass
    
    def handleRequest(self, data: dict) -> None:
        pass
