
from user import User
from post import Post
from follow import Follow

class Serialiser:
    
    def __init__(self) -> None:
        pass
    
    def createPost(self, user_uid: str, post_text: str) -> Post:
        pass
    
    def createUser(self, nickname: str, pubkey: str) -> User:
        pass
    
    def createFollow(self, who: str, whom: str) -> Follow:
        pass
    
    def getFollow(self, uid: str) -> Follow:
        pass

    def getPost(self, uid: str) -> Post:
        pass
    
    def getPosts(self, uid: str) -> list[str]:
        pass
    
    def getUser(self, uid: str) -> User:
        pass
