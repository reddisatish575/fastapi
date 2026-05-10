from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import Depends, status, HTTPException, APIRouter
from ..utils import hash_password


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db : Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users

@router.get("/{id}", response_model=schemas.UserResponse)
def get_users(id : int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id : {id} does not exist")
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user : schemas.UserBody, db : Session = Depends(get_db)):
    #hash the password 
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user