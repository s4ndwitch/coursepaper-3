
class Post:
    
    _uid: str
    _signature: str
    _author: str
    _text: str
    
    def __init__(self, uid: str, signature: str, author: str, text: str) -> None:
        
        self._uid = uid
        self._signature = signature
        self._author = author
        self._text = text
