
class User:
    
    uid: str
    nickname: str
    pubkey: str
    
    def __init__(self, uid: str, nickname: str, pubkey: str) -> None:
        
        self.uid = uid
        self.nickname = nickname
        self.pubkey = pubkey
