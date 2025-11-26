from src.restaurant_review_system.repository.signin import SignIn

from src.restaurant_review_system.schemas.login import UserLogin,ChangePassword
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.restaurant_review_system.authorization.auth import create_token
from src.restaurant_review_system.utils.response import Response
from src.restaurant_review_system.schemas.login import UpdateInfo


response=Response()
signin_repo=SignIn()


class SignInService:

    def customer(self,user:UserLogin,db:Session):
        try:
                
            role="customer"
            db_user=signin_repo.user_data(user,db)
            if db_user:
                return response.sucess_response("Customer already exists",403)
            else:
                signin_repo.add_user(user,role,db)
                
                return response.sucess_response("Customer Sucessfully Registered")       
        except Exception as e:
             return response.error_response(str(e))
            

    def owner(self,user:UserLogin,db:Session):
            try:
                    
                role="owner"
                db_user=signin_repo.user_data(user,db)
                if db_user:
                    return response.error_response("Owner already exists",403)
                else:
                    signin_repo.add_user(user,role,db)
                    return response.sucess_response("Owner Added Sucessfully")
            except Exception as e:
                 return response.error_response(str(e))
                

         
    def login(self,user,db:Session):
            try:
                 
                db_user=signin_repo.user_data(user,db)
                if not db_user:
                    raise HTTPException(status_code=404,detail="Wrong Username")
                db_password=signin_repo.user_data_pass(user,db)
                if not db_password:
                    raise HTTPException(status_code=404,detail="Wrong Password")
                token=create_token(db_user.role,db_user.user_id)

                result= {
                    "msg":"Logged in Successfully",
                    "token":token,
                    "role":db_user.role,
                    "user_id":db_user.user_id
                }
                return response.sucess_response(result)
            except Exception as e:
                 return response.error_response(str(e))
    

    def change_passowrd(self,user:ChangePassword,db:Session):
         try:
              
            db_user=signin_repo.user_data(user,db)
            if not db_user:

                return response.error_response("Wrong Username")
            
            db_password=signin_repo.check_password(user,db)
            if not db_password:

                return response.error_response("Wrong Old Password")
            db_user.password=user.new_password
            db.commit()
            return response.sucess_response("Password Updated Sucessfully")
            
         
         except Exception as e:
              return response.error_response(str(e))
         
    def update_info(self,user_id,user:UpdateInfo,db:Session):
         try:
              db_user=signin_repo.update_info(user_id,db)
              if not db_user:
                   return response.error_response("No such user",404)
              if user.username is not None:
                   db_user.username=user.username.lower()

              if user.password is not None:
                   db_user.password=user.password.lower()

              db.commit()
              return response.sucess_response("User Updated Sucessfully")
         except Exception as e:
              return response.error_response(str(e))

                   
    def delete_user(self,user_id,db:Session):
         try:
              db_user=signin_repo.delete_user(user_id,db)
              if not db_user:
                   return response.error_response("No Such User")
              signin_repo.delete_user_commit(db_user,db)


              return response.sucess_response("Sucessfully Deleted User")
              
         except Exception as e:
              return response.error_response(str(e))
              
         
