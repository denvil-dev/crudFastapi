from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str


class userLogin(BaseModel):
    email: str
    password: str

class Config:
        orm_mode = True