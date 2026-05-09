from fastapi import Depends, FastAPI, Response, status, HTTPException
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi.params import Body
from . import models, schemas
from .database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

# try:
#     conn = psycopg2.connect(host="localhost",database="fastapi",
#                             user="reddisatish", password="postgres",
#                             cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Database Connection Successful")
# except Exception as error:
#     print("Connecting to database failed")
#     print("Error :: ", error)
#     time.sleep(5)

my_posts = [
    {
        "title":"Modern Java",
        "content":"This is java",
        "id":1
    },
     {
        "title":"Modern Python",
        "content":"This is Python",
        "id":2
    },
     {
        "title":"Modern Angular",
        "content":"This is Angular",
        "id":3
    }
]

@app.get("/")
def root():
    return {"message":"Hello World"}

# @app.get("/posts")
# def get_posts():
#     cursor.execute(""" SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print(posts)
#     print(f"Type of posts {type(posts)}")
#     return {"data": posts}

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def add_post(post:Post):
#     # new_post=post.model_dump()
#     # new_post["id"]=random.randint(100,1000)
#     # my_posts.append(new_post)
#     # return {"data" : my_posts}
#     cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) 
#                    RETURNING * """,
#                    ( post.title, post.content, post.published ))
#     new_posts=cursor.fetchone()
#     conn.commit()
#     return {"data":new_posts}
#     # new_posts=get_posts()
#     # return new_posts

@app.post("/createPost")
def create_posts(postData : dict = Body(...)):
    print("uix postData ::: ", postData, type(postData))
    return {"message": "Posts Created Successfully"}

@app.get("/posts/latest")
def getLatestPost():
    post = findLatestPost()
    return {"post_detail":post}

# @app.get("/posts/{id}")
# def getPostById(id : str):
#     print("path variable ::: ", id)
#     # post = findPostById(id)
#     cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
#     post = cursor.fetchone()
#     if not post:
#         # response.status_code= status.HTTP_404_NOT_FOUND
#         # return {"message": f"post with id {id} was not found"}
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                             detail = f"post with id {id} was not found")
#     return {"post_detail":post}

# @app.delete("/posts/{id}")
# def deletePost(id : str):
#     # index = findIndexByPostId(id)
#     # print("index ::: ", index)
#     # if index is None:
#     #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#     #         detail=f"post with {id} is not found")
#     # return {"post_detail": my_posts}
#     # my_posts.pop(index)
#     cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
#     deletedPost = cursor.fetchone()
#     conn.commit()
#     if deletedPost is None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                         detail = f"post with id {id} was not found")
#     return {"post_detail":deletedPost}
    

# @app.put("/posts/{id}")
# def updatePost(id : int, post : Post):
#     # print(f"Before Model Dum :: {post}")
#     # newPost = post.model_dump()
#     # print(f"After Model Dum :: {newPost}")
#     # index = findIndexByPostId(id)
#     # if index is None:
#     #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#     #         detail=f"post with {id} is not found")
#     # newPost["id"]=id
#     # my_posts[index]=newPost
#     # return {"post_detail": my_posts}
#     cursor.execute(""" UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (post.title, post.content, id, ))
#     update_post = cursor.fetchone()
#     if update_post is None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#                         detail = f"post with id {id} was not found")
#     conn.commit()
#     return {"post_detail":update_post}



# Write Common Methods Below


def findLatestPost():
    return my_posts[-1]

def findPostById(id):
    for item in my_posts:
        if item["id"]==id:
            return item

def findIndexByPostId(id):
    for ind, post in enumerate(my_posts):
        if post["id"]==id:
            return ind
        return None
    
# =====================================
# SQLAlchemy

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts  = db.query(models.Post).all()

    return {"status":"Successful", "data": posts}

@app.get("/posts", response_model= list[schemas.Post])
def get_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    # print(f"Type of posts {type(posts)}")
    # return {"data": posts}
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def add_post(post: schemas.CreatePost, db : Session = Depends(get_db)):
    # print("python add post ::: ", post.model_dump())
    # print("python add post dict::: ", post.dict())
    # new_post = models.Post(title=post.title, content = post.content, published= post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(f"Type of post {type(new_post)}")
    # return {"data": new_post}
    return new_post

@app.get("/posts/{id}", response_model=schemas.Post)
def getPostById(id : str, db : Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} was not found")
    # return {"post_detail":post}
    return post

@app.delete("/posts/{id}", response_model=schemas.Post)
def deletePost(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found"
        )
    deletedPost = post
    db.delete(post)
    db.commit()
    # return {"post_detail": deletedPost}
    return deletedPost

@app.put("/posts/{id}", response_model=schemas.Post)
def updatePost(id : int, post : schemas.UpdatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = post_query.first()
    if update_post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"post with id {id} was not found")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()    
    # return {"post_detail":post_query.first()}
    return post_query.first()