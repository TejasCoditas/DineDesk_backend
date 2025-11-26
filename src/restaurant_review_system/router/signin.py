from fastapi.routing import APIRouter
from src.restaurant_review_system.backend.config import get_db

from src.restaurant_review_system.schemas.login import UserLogin,ChangePassword,UpdateInfo
from sqlalchemy.orm import Session
from fastapi import Depends
from src.restaurant_review_system.authorization.auth import validate_token

from src.restaurant_review_system.services.sigin import SignInService




router=APIRouter(prefix="/register",tags=["Register"])

singnin_service=SignInService()

@router.post("/signup/customer")
async def signup(user:UserLogin,db:Session=Depends(get_db)):
    return singnin_service.customer(user,db)
    

@router.post("/signup/owner")
async def signup(user:UserLogin,db:Session=Depends(get_db)):
    return singnin_service.owner(user,db)


@router.post("/login")
async def Register(user:UserLogin,db:Session=Depends(get_db)):
    login_details=singnin_service.login(user,db)

    return login_details

# @router.put("/changepassweord")
# async def change_password(user:ChangePassword,db:Session=Depends(get_db)):
        
#         password=singnin_service.change_passowrd(user,db)
#         return password


     
@router.put("/update")
async def update_details(user:UpdateInfo,db:Session=Depends(get_db),payload:dict=Depends(validate_token(["owner","admin","customer"]))):
     user_id=payload.get("sub")
     update_int=singnin_service.update_info(user_id,user,db)
     return update_int
     
     

     
@router.delete("/delete/user")
async def delete_user(user_id:int,db:Session=Depends(get_db)):
     db_user=singnin_service.delete_user(user_id,db)
     return  db_user
     

