from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, create_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import engine

db_engine = None

def init_engine(uri, **kwargs):
    global db_engine
    db_engine = create_engine(uri, **kwargs)
    return db_engine


Session = scoped_session(lambda: create_session(bind=db_engine,
                                                autoflush=True,
                                                autocommit=False,
                                                expire_on_commit=True))
Base = declarative_base()
Base.query = Session.query_property()

