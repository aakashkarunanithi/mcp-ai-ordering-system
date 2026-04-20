from contextlib import contextmanager
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, Session
from settings import config
from typing import Generator, AsyncGenerator, Any
from sqlalchemy.engine import Engine, Inspector
from utils.exceptions.custom_app_exception import Custom_App_Exception
from utils.exceptions.error_codes import ErrorCode
from utils.exceptions.http_status import HttpStatusCode


class Database:
    _instance = None

    def __new__(cls):
        """Ensures only one instance of database exists"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
            
    def __init__(self):
        if self._initialized:
            return 
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False
        )
        self._initialized = True
    
    @contextmanager
    def get_db(self)-> Generator[Session,None, None]:
        """Provides a databse session as a context manager"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def _create_engine(self)-> Engine:
        """Creates and return a SQLAlchemy database engine"""
        db_url = (
            f"postgresql+psycopg2://{config.db_username}:"
            f"{config.db_password}@"
            f"{config.db_host}:"
            f"{config.db_port}/"
            f"{config.db_name}"
        )
        return create_engine(db_url)

    async def get_session(self)-> AsyncGenerator[Session, None]:
        """Provides a database session as an async context manager"""
        try:
            session = self.SessionLocal()
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    def inspector(self, engine)-> Inspector:
        """Returns a SQLAlchemy inspector for schema inspection"""
        return inspect(engine)
    
    async def test_connection(self)-> bool:
        """Tests database connection and returns True if successful"""
        try:
            with self.engine.connect() as connection:
                connection.execute(text(" SELECT 1"))
            return True
        
        except Exception :
            raise Custom_App_Exception(
            message=f"DB Connection Failed",
            code=ErrorCode.DB_CONNECTION_FAIL,
            status_code=HttpStatusCode.SERVICE_UNAVAILABLE,
        )