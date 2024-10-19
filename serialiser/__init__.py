
from serialiser.user import User
from serialiser.post import Post
from hashlib import sha256

import serialiser.orm as orm

class Serialiser:

    _orm: orm.Session
    
    def __init__(self, db_file:str = "db.sqlite") -> None:

        orm.orm_init(db_file)

        self._orm = orm.create_session()
    
    def createPost(self, author: str, text: str, signature: str, uid: str = None) -> Post:

        if uid == None:
            uid = sha256((author + text).encode()).hexdigest()

        post = Post(
            uid=uid,
            author=author,
            text=text,
            signature=signature
        )

        orm_post = orm.Post(
            uid=uid, author=author, text=text, signature=signature
        )
        self._orm.add(orm_post)
        self._orm.commit()

        return post

    def createUser(self, nickname: str, pubkey: str, uid: str = None) -> User:

        if uid == None:
            uid = sha256((nickname + pubkey).encode()).hexdigest()

        user = User(
            uid=uid, nickname=nickname,
            pubkey=pubkey
        )

        orm_user = orm.User(
            uid=uid, nickname=nickname,
            pubkey=pubkey
        )
        self._orm.add(orm_user)
        self._orm.commit()

        return user

    def getPost(self, uid: str) -> Post:

        orm_post = self._orm.query(orm.Post).filter(
            orm.Post.uid == uid
        ).first()
        
        if orm_post == None:
            return None

        post = Post(
            uid=orm_post.uid,
            author=orm_post.author,
            text=orm_post.text,
            signature=orm_post.signature
        )

        return post
    
    def getPosts(self, uid: str) -> list[str]:

        orm_posts = self._orm.query(
            orm.Post
        ).filter(
            orm.Post.author == uid
        ).all()

        return list(map(lambda x: x.uid, orm_posts))
    
    def getUser(self, uid: str) -> User:
        
        orm_user = self._orm.query(orm.User).filter(
            orm.User.uid == uid
        ).first()
        
        if orm_user == None:
            return None
        
        user = User(
            uid=orm_user.uid,
            nickname=orm_user.nickname,
            pubkey=orm_user.pubkey
        )
        
        return user
