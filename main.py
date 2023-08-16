from typing import Optional
from fastapi import Body, FastAPI,status,HTTPException
from pydantic import BaseModel
import uuid

app =FastAPI()


class Post(BaseModel):
    title:str
    content:str
    published:bool|None = False
    rating:int|None = 3


my_posts = []

def find_post(id:str):
    for post in my_posts:
        print(post)
        if str(post['id']) == id:
            return post


def find_post_id(id:str):
    for index,post in enumerate(my_posts):
        if str(post['id']) == id:
            return index


@app.get("/")
async def root():
    return {"message":"Welcome to my apis"}

@app.get("/posts")
def get_posts():
    return {"posts":my_posts}

@app.get("/posts/{id}")
def get_posts(id:uuid.UUID):
    post = find_post(str(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {str(id)} not found")
    return {
        "post":post
    } 
          


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(new_post:Post):
    new_post = new_post.model_dump()
    my_posts.append(new_post)
    new_post['id'] = uuid.uuid4()
    return {"posts":my_posts}

@app.delete("/posts/{id}")
def delete(id:uuid.UUID):
    post_index = find_post_id(str(id))
    if not post_index and post_index!=0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with ID {str(id)} not found")
    del my_posts[post_index]
    return {
        "message":"Post was successfully deleted"
    }

