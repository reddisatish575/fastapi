from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional

# Request Modesl

class Post(BaseModel):
    title : str
    content:str
    published : bool = True 
    # rating : optional[int] = None
    rating : int | None = None

class CreatePost(BaseModel):
    title : str
    content: str

class UpdatePost(BaseModel):
    title : str
    content: str

class PostBase(BaseModel):
    title : str
    content:str
    published : bool = True 

class CreatePostBase(PostBase):
    pass


# Response Models

class Post(PostBase):
    id : int
    # title : str
    # content:str
    # published : bool
    created_at : datetime

    # old pydantic
    # class Config:
    #     orm_mode = True

    #new pydantic
    model_config = ConfigDict(from_attributes=True)

# Users schemas
#Request model
class UserBody(BaseModel):
    # email : str
    email : EmailStr
    password : str

#Response Model 
class UserResponse(BaseModel):
    id : int 
    email : EmailStr
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)


# Login Schemas

class UserLogin(BaseModel):
    email :str 
    password :str
    
class Token(BaseModel):
    access_token :str
    token_type:str

class TokenData(BaseModel):
    id : str | None = None


