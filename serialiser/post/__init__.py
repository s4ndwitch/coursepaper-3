
class Post:
    
    uid: str
    signature: str
    author: str
    text: str
    
    def __init__(self, uid: str, signature: str, author: str, text: str) -> None:
        
        self.uid = uid
        self.signature = signature
        self.author = author
        self.text = text
