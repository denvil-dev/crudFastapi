from fastapi import APIRouter, Depends, HTTPException, status
from database.database import get_db, Base
from schemas.userSchema import User
from sqlalchemy.orm import Session
from models.userModel import UserCreate 


registerRouter = APIRouter()


@registerRouter.post("/register")
async def register (user: UserCreate, db: Session = Depends(get_db)):
    findUser = db.query(User).filter(User.email == user.email).first()
    if findUser:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    newUser = User(
        name=user.name,
        email=user.email,
        password=user.password,
        role=user.role
    )
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return {"message": "User registered successfully", "user_id": newUser.id}
