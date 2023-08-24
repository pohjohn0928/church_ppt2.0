from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mysql import Base
from settings import DBSettings
from sqlalchemy_utils import database_exists, create_database
settings = DBSettings()


class DBInit(object):
    def __init__(self):
        self.engine = create_engine(settings.DB_URL)
        self.session = sessionmaker(bind=self.engine)

    def __enter__(self):
        self.session = self.session()
        return self

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def __exit__(self, _type, value, trace):
        self.session.commit()
        self.session.close()


if not database_exists(settings.DB_URL):
    db = DBInit()
    create_database(db.engine.url)
    db.create_table()
#
# db = DBInit()
# db.create_table()
