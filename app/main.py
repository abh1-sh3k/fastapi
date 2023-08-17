from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import uuid
import psycopg2

# returns value from database in dict format
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool | None = False
    rating: int | None = 3


my_posts = []
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="root@123",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successfully!")
        break
    except Exception as e:
        print("Connection failed!!!")
        print(e)
        time.sleep(2)


def find_post(id: str):
    for post in my_posts:
        print(post)
        if str(post["id"]) == id:
            return post


def find_post_id(id: str):
    for index, post in enumerate(my_posts):
        if str(post["id"]) == id:
            return index


@app.get("/")
async def root():
    return {"message": "Welcome to my apis"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"posts": posts}


@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute(
        """
SELECT * FROM posts WHERE id = %s
""",
        (str(id)),
    )
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {str(id)} not found",
        )
    return {"post": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    cursor.execute(
        """
INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING *
""",
        (new_post.title, new_post.content, new_post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"post": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    cursor.execute(
        """
DELETE FROM posts WHERE id = %s RETURNING *
""",
        (str(id)),
    )
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {str(id)} not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """
        UPDATE posts
        SET title = %s,content= %s,published = %s
        WHERE id = %s
        RETURNING *          
""",
        (post.title, post.content, post.published, str(id)),
    )
    conn.commit()
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {str(id)} not found",
        )
    return {"updated post": updated_post}
