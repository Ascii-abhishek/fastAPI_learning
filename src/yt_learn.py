from typing import Annotated, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Query, Response, status, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()
my_posts = [
    {"id": 1, "title": "title of post 1", "content": "content of post 1"},
    {"id": 2, "title": "title of post 2", "content": "content of post 2"},
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


# this is used for data validation
class Post(BaseModel):
    title: str
    content: str
    publish: bool = True  # using default value
    # extra: str | None = "optional"  -> Optional field, user may or may not send
    extra_2: Optional[int] = None  # also optional
    # ann_ext = Annotated[str | None]


try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='56987', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Databse connection successful")
except Exception as error:
    print("connectiopn failed: ", error)



@app.get("/allposts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_posts(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post not found"}
    return {"data": post}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    # return {"data": post_dict}
    return JSONResponse(
        content={"data": post_dict}, status_code=status.HTTP_201_CREATED
    )


@app.delete("/posts/{id}")
def delete_code(id: int):
    index = find_index_post(id)
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist",
        )
    my_posts.pop(index)
    # return {"message": "post deleted successfully"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist",
        )
    my_posts[index].update(post.model_dump())
    return JSONResponse(
        content={"data": my_posts[index]}, status_code=status.HTTP_202_ACCEPTED
    )
