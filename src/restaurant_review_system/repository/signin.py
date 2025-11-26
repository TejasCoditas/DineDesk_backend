from sqlalchemy.orm import Session
from src.restaurant_review_system.backend.models import User
from src.restaurant_review_system.schemas.login import UserLogin,ChangePassword

class SignIn:
    def user_data(self,user:UserLogin,db:Session):
        db_user=db.query(User).filter(User.username==user.username).first()     
        return db_user 
        
    def add_user(self,user:UserLogin,role,db:Session):
         user_details=User(role=role,username=user.username.lower(),
                           password=user.password)
         db.add(user_details)
         db.commit()
         return user_details
    
    # def add_user_owner(self,user:UserLogin,db:Session):
    #      user_details=User(role="owner",username=user.username,password=user.password)
    #      db.add(user_details)
    #      db.commit()
    #      return user_details

    def user_data_pass(self,user:UserLogin,db:Session):
        db_user=db.query(User).filter(User.password==user.password).first()     
        return db_user 
        
    
 
    def check_password(self,user:ChangePassword,db:Session):
         db_password=db.query(User).filter(User.password==user.old_password).first()

         return db_password
    
    def update_info(self,user_id,db:Session):
        db_user=db.query(User).filter(User.user_id==user_id).first()
        return db_user
    
    def delete_user(self,user_id,db:Session):
        db_user=db.query(User).filter(User.user_id==user_id).first()
        return db_user
    
    def delete_user_commit(self,db_user,db:Session):
        db.delete(db_user)
        db.commit()