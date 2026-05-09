from pydantic import BaseModel, ConfigDict
from datetime import datetime
# from typing import Optional

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



