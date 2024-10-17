
class User:
    
    _uid: str
    _nickname: str
    _pubkey: str
    
    def __init__(self, uid: str, nickname: str, pubkey: str) -> None:
        
        self._uid = uid
        self._nickname = nickname
        self._pubkey = pubkey
