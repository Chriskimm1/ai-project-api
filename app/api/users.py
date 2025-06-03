from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

router = APIRouter()

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

# Create tables
Base.metadata.create_all(bind=engine)

class User(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    db_user = UserDB(id=user.id, name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[User])
def read_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}