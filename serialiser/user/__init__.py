
from rsa import PublicKey

class User:
    
    _uid: str
    _nickname: str
    _pubkey: PublicKey
    
    def __init__(self, uid, nickname, pubkey) -> None:
        
        self._uid = uid
        self._nickname = nickname
        self._pubkey = pubkey
