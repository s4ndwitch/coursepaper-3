from sqlalchemy import Column, Text, String, ForeignKey
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
