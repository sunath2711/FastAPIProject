from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"  #only changing this for PostgresSQL would work too

engine = create_engine(  #engine here is the connection to database
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  #creates a database session


class Base(DeclarativeBase):
    pass


def get_db():
    with SessionLocal() as db:
        yield db