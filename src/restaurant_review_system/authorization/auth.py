from jose import jwt,JWTError
from datetime import datetime,timedelta
from fastapi import Depends
from fastapi import HTTPException
import os
from dotenv import load_dotenv
load_dotenv()

ALGORITHM=os.getenv("ALGORITHM")
SECRET_KEY=os.getenv("SECRET_KEY")


from fastapi.security import OAuth2PasswordBearer

outh_schemas=OAuth2PasswordBearer(tokenUrl="/")


def create_token(role,user_id):
    if role:
        data={
            "iss":"fastapi-auth-sever",
            "role":role,
            "sub":str(user_id),
            "aud":"fastapi-clients",
            "iat":datetime.now().timestamp(),
            "exp":datetime.now().timestamp()+timedelta(minutes=15000).total_seconds()
        }

        token=jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
        return token


def validate_token(access_list: list):

    def decode_token(token=Depends(outh_schemas)):
        try:
            payload=jwt.decode(token,key=SECRET_KEY,
                            issuer="fastapi-auth-sever",
                            audience="fastapi-clients",
                            algorithms=[ALGORITHM])
            
            role=payload.get("role")
            user_id=payload.get("sub")
            if role is None:
                raise HTTPException(status_code=404,detail="No username found")
            
            if role not in access_list:
                raise HTTPException(status_code=403,detail="Access Restricted")

            return {
                "role":role,
                "sub":user_id
            }

        except JWTError:
            raise HTTPException(status_code=404,detail="Token  has Expired")
        
    return decode_token