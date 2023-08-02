from typing import Annotated, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Query, Response, status, HTTPException, Depends
from fastapi.responses import JSONResponse
import uvicorn
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# this is used for data validation
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # using default value
    # extra: str | None = "optional"  -> Optional field, user may or may not send
    # extra_2: Optional[int] = None  # also optional
    # ann_ext = Annotated[str | None]


try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="56987",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Databse connection successful")
except Exception as error:
    print("connectiopn failed: ", error)
    time.sleep(2)


@app.get("/allposts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts""")
    # my_posts = cursor.fetchall()
    my_posts = db.query(models.Post).all()
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_posts(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""  SELECT * from posts where id = %s""", str(id))
    # my_post = cursor.fetchone()
    my_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not my_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    return {"data": my_post}


@app.post("/posts")
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published),
    # )
    # my_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
    # return JSONResponse(
    #     content={"data": my_post}, status_code=status.HTTP_201_CREATED
    # )


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""  DELETE from posts where id = %s RETURNING *""", str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_posts = db.query(models.Post).filter(models.Post.id == id)
    if not deleted_posts.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist",
        )
    deleted_posts.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """UPDATE posts set title = %s, content = %s, published = %s where id = %s RETURNING * """,
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_posts = db.query(models.Post).filter(models.Post.id == id)
    if updated_posts.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist",
        )
    
    updated_posts.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"data": updated_posts.first()}
