from fastapi import APIRouter, Form, Depends, HTTPException
from auth import authenticate_user, create_token
from database.database import get_db
from sqlalchemy.orm import Session

loginRouter = APIRouter()


@loginRouter.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token_data = {
        "sub":user.email,
        "password":user.hashed_password,
        "role":user.role,
        "id":user.id
    }
    token = create_token(token_data)


    return {"access_token": token, "token_type": "bearer"}
