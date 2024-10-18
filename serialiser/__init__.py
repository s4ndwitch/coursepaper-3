
from user import User
from post import Post
from hashlib import sha256

import orm

class Serialiser:

    _orm: Session
    
    def __init__(self, db_file:str = "db.sqlite") -> None:

        global_init(db_file)

        self._orm = create_session()
    
    def createPost(self, author: str, text: str) -> Post:

        uid = sha256(author + text)

        post = Post(uid=uid,
                author=author, text=text)

        orm_post = orm.Post(
            uid=uid, author=author, text=text
        )
        self._orm.add(orm_post)
        self._orm.commit()

        return post

    def createUser(self, nickname: str, pubkey: str) -> User:

        uid = sha256(nickname + pubkey)

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

        post = Post(
            uid=orm_post.uid,
            author=orm_post.author,
            text=orm_post.tedt
        )

        return post
    
    def getPosts(self, uid: str) -> list[str]:

        orm_posts = self._orm.query(
            orm.Post
        ).filter(
            orm.Post.author == uid
        ).all()

        return list(orm_posts)
    
    def getUser(self, uid: str) -> User:
        pass
