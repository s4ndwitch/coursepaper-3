
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from sqlalchemy import Column, Text, String, ForeignKey
from sqlalchemy_serializer import SerializerMixin

SqlAlchemyBase = declarative_base()


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "users"
    uid = Column(String, primary_key=True)
    nickname = Column(String)
    pubkey = Column(Text, unique=True)


class Post(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "posts"
    uid = Column(String, primary_key=True)
    author = Column(String, ForeignKey("users.uid"))
    text = Column(Text)
    signature = Column(Text)


__factory = None


def orm_init(db_file):
    
    global __factory
    
    if __factory:
        return
    
    if not db_file or not db_file.strip():
        raise Exception("No fileway.")
    
    conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    
    orm_engine = create_engine(conn_str, echo=False)
    __factory = sessionmaker(bind=orm_engine)
    
    SqlAlchemyBase.metadata.create_all(orm_engine)


def create_session() -> Session:
    global __factory
    return __factory()
