from contextlib import contextmanager
from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session

from app.core.setting import setting


class Database:
    def __init__(self):
        self.engine = create_engine(setting.get_db_url, pool_size=10, max_overflow=15, pool_recycle=3600)
        self.session_factory = orm.scoped_session(
            orm.sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

    @contextmanager
    def session(self):
        session: Session = self.session_factory()
        try:
            yield session
        except Exception as e:
            print('Session rollback because of exception: %s', e)
            session.rollback()
        finally:
            session.close()

database = Database()