from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from typing import Generator

from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)


@event.listens_for(engine, "connect")
def _register_unicode_lower(dbapi_connection, connection_record):
    """SQLite по умолчанию умеет приводить к нижнему регистру только ASCII.
    Регистрируем Python-функции lower/upper для корректной поддержки кириллицы.
    """
    dbapi_connection.create_function("lower", 1, lambda s: s.lower() if isinstance(s, str) else s)
    dbapi_connection.create_function("upper", 1, lambda s: s.upper() if isinstance(s, str) else s)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
