
from user import User
from action.post import Post
from action.like import Like
from action.follow import Follow

class Serialiser:
    
    def __init__(self) -> None:
        pass
    
    def createLike(self, user_uid: str, post_uid: str) -> Like:
        pass
    
    def createPost(self, user_uid: str, post_text: str) -> Post:
        pass
    
    def createUser(self, nickname: str, pubkey: str) -> User:
        pass
