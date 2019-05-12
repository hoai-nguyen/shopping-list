from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, create_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import engine
from sqlalchemy.schema import (
    MetaData,
    Table,
    DropTable,
    ForeignKeyConstraint,
    DropConstraint,
)

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


def init_db():
    import analysis_interface.models
    Base.metadata.create_all(db_engine)


def drop_db():
    if db_engine is None:
        raise Exception
    conn = db_engine.connect()
    trans = conn.begin()
    inspector = engine.reflection.Inspector.from_engine(db_engine)

    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []

        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(ForeignKeyConstraint((), (), name=fk['name']))
        t = Table(table_name, metadata, *fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()
