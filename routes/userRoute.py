from database.database import Base, get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.userSchema import User as userDb
from models.userModel import UserCreate
from auth import require_role


userRouter = APIRouter()


@userRouter.get("/users")
async def create_user( db: Session = Depends(get_db)):
    users = db.query(userDb).all() 

    return users    

@userRouter.post ("/addUser")
async def create_user (user: UserCreate,token: dict  =Depends (require_role(["admin"])), db: Session  =Depends (get_db) ):

    return {"message":"User created successfully"}


@userRouter.put("/updateUser/{user_id}")
async def update_user(user_id: int, user: UserCreate, token: dict = Depends(require_role(["admin", "user"])), db:Session = Depends(get_db)):
    if token["role"] != "admin" and token["id"]!=user_id:
        raise HTTPException (status_code=304, detail="This is not your account")


    existing_user = db.query(userDb).filter(userDb.id == user_id).first()


    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.password = user.password
    existing_user.role = user.role

    db.commit()
    db.refresh(existing_user)
    return {"message": "User updated successfully", "user_id": existing_user.id}


@userRouter.delete("/deleteUser/{user_id}")
async def delete_user(user_id: int, token: dict = Depends(require_role(["admin","user"])), db: Session = Depends(get_db)):
    if token["role"] != "admin" and token["id"]!=user_id:
        raise HTTPException (status_code=304, detail="This is not your account")
    findUser = db.query(userDb).filter(userDb.id == user_id).first()

    if not findUser:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(findUser)
    db.commit()
    return {"message": "User deleted successfully"}