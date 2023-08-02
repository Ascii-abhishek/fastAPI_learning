from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from database import engine
from routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)

# try:
#     conn = psycopg2.connect(
#         host="localhost",
#         database="fastapi",
#         user="postgres",
#         password="56987",
#         cursor_factory=RealDictCursor,
#     )
#     cursor = conn.cursor()
#     print("Databse connection successful")
# except Exception as error:
#     print("connectiopn failed: ", error)
#     time.sleep(2)





