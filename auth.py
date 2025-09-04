from fastapi import HTTPException, Depends
from jose import JWTError, jwt
from schemas.userSchema import User
from fastapi.security import OAuth2PasswordBearer
import os 
from dotenv import load_dotenv     

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")



def create_token (data:dict):
    to_encode = data.copy()
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def authenticate_user (db, email:str, password:str):
    user = db.query(User).filter(User.email == email).first()
    if not user: 
        return False
    return user

def decode_token (token:str = Depends(oauth2_scheme)):
    try:

        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        password : str = payload.get("password")
        role:str = payload.get("role")
        id: int =payload.get("id") 


    except JWTError:
        print(JWTError)

def require_role (role: list[str]):
    def role_checker(token: dict = Depends(decode_token)):
        if token["role"] not in role:
            raise HTTPException(status_code=403, detail="No permission")
        return token
    return role_checker
       