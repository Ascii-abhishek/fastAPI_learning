from pydantic import BaseModel, EmailStr
from datetime import datetime

# this is used for data validation
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
# extra: str | None = "optional"  -> Optional field, user may or may not send
# extra_2: Optional[int] = None  # also optional
# ann_ext = Annotated[str | None]


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
