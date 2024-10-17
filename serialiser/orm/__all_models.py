from sqlalchemy import Column, Integer, Text, DateTime, String, Boolean, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from .__init__ import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "users"
    uid = Column(String, primary_key=True)
    nickname = Column(String, unique=True)
    pubkey = Column(Text, unique=True)


class Post(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "posts"
    uid = Column(String, primary_key=True)
    author = Column(String, ForeignKey("users.uid"))
    text = Column(Text)
    signature = Column(Text)

class Like(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "likes"
    author = Column(String, ForeignKey("users.uid"))
    post = Column(String, ForeignKey("posts.uid"))
    signature = Column(Text)

class Follow(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "likes"
    who = Column(String, ForeignKey("users.uid"))
    whom = Column(String, ForeignKey("users.uid"))
    signature = Column(Text)
