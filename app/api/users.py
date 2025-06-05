from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import UserDB, User, UserCreate, get_db
from uuid import uuid4
from app.api.auth import hash_password

router = APIRouter()

@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check for duplicate email
    if db.query(UserDB).filter(UserDB.email == user.email).first():
        raise HTTPException(status_code=400, detail="User with this email already exists")
    # Generate a UUID for user.id
    user_id = str(uuid4())
    hashed_password = hash_password(user.password)
    db_user = UserDB(id=user_id, name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#Debating if this is even needed 
@router.get("/users/", response_model=List[User])
def read_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = hash_password(user.password)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error: duplicate id or email")

@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}