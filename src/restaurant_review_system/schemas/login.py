from pydantic import Field,BaseModel
from src.restaurant_review_system.utils.validation import Validation
from typing import Optional

class UserLogin(Validation):
    username:str=Field(min_length=6,max_length=40,pattern=r"^[A-Za-z0-9@.$!%*?&]+$")
    password:str=Field(min_length=6,max_length=40,pattern=r"^[A-Za-z0-9@$!%*?&]+$")


class ChangePassword(Validation):
    username:str=Field(min_length=6,max_length=40,pattern=r"^[A-Za-z0-9@.$!%*?&]+$")
    old_password:str=Field(min_length=6,max_length=40,pattern=r"^[A-Za-z0-9@$!%*?&]+$")
    new_password:str=Field(min_length=6,max_length=40,pattern= r"^[A-Za-z0-9@$!%*?&]+$")

class UpdateInfo(BaseModel):

    username:Optional[str]=Field(default=None,min_length=0,max_length=40,pattern=r"^[A-Za-z0-9@.$!%*?&]+$")
    password:Optional[str]=Field(default=None,min_length=0,max_length=40,pattern=r"^[A-Za-z0-9@$!%*?&]+$")



