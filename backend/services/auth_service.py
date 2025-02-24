from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..models.user_model import User
import os
import smtplib
from datetime import datetime,timedelta
from typing import Annotated 


from ..dependencies import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES, logger

from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
from jose import jwt,JWTError


from email.message import EmailMessage


oauth2_bearer=OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)



def authenticate_user(email:str,password:str,db):
   user=db.query(User).filter(User.email==email).first()
   if not user or not verify_password(password, user.password_hash):
     return False
   return user




def create_access_token(email:str,id:int,role:str, expires_delta: timedelta = None):
    to_encode = {
        "sub":email,
        "id":id,
        "role":role,
    }
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
   try:
      payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
      email=payload.get('sub')
      id=payload.get('id')
      role=payload.get('role')
      if email is None or id is None :
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')
      return{'email':email, 'id':id,'role':role}
   except JWTError:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Token expired')