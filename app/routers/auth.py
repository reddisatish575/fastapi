from fastapi import HTTPException, APIRouter, Depends, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas, models, database, utils, oauth2

router = APIRouter(prefix="/auth", tags=["Authentication"])


# @router.post("/login")
# def login(user_creds : schemas.UserLogin, db : Session = Depends(database.get_db)):

#     user = db.query(models.User).filter(models.User.email == user_creds.email).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
#     if not utils.verify_password(user_creds.password, user.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
#     # create a token 
#     access_token = oauth2.create_access_token(data = {"user_id":user.id})
#     # return token

#     return {"access_token" : access_token, "token_type": "bearer"}

@router.post("/login")
# def login(user_creds : schemas.UserLogin, db : Session = Depends(database.get_db)):
def login(user_creds : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_creds.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not utils.verify_password(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    # create a token 
    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    # return token

    return {"access_token" : access_token, "token_type": "bearer"}

