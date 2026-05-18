from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from backend.config.settings import settings

DATABASE_URL = (
    f"mysql+mysqlconnector://"
    f"{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}"
    f"/{settings.DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,     # auto-reconnect if connection drops
    pool_size=5,
    echo=False              # set True to log all SQL (debug only)
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models


class Base(DeclarativeBase):
    pass


def get_db():
    """
    Yields a DB session for each request, closes it when done.
    Use as:  db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Automatically create tables based on ORM models if they don't exist
def init_db():
    from backend.models.schema import User, ChatHistory
    Base.metadata.create_all(bind=engine)
    print("Tables created / verified.")
