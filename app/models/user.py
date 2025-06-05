from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel
from typing import Optional
import uuid

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    internal_id = Column(Integer, primary_key=True, index=True)
    id = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))  # UUID as string
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class User(BaseModel):
    id: str  # UUID string
    name: str
    email: str
    # internal_id and password are not exposed in API responses

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()