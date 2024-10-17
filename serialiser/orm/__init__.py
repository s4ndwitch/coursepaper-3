
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import dec
from sqlalchemy.orm import sessionmaker, Session

SqlAlchemyBase = dec.declarative_base()

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
    
    from . import __all_models
    
    SqlAlchemyBase.metadata.create_all(orm_engine)


def create_session() -> Session:
    global __factory
    return __factory()
