from pydantic import BaseModel,Field
from src.restaurant_review_system.utils.validation import Validation
from typing import List,Optional

class RestaurantCreate(Validation):
    restaurant_name:str=Field(min_length=5,max_length=250)
    address:str=Field(min_length=5,max_length=250)
    contact:str=Field(pattern=r"^(\+91[\-\s]?)?[0]?(91)?[6789]\d{9}$")
    image_url:Optional[str]=None

class RestaurantUpdate(BaseModel):
    restaurant_name:Optional[str]=Field(default=None,min_length=5,max_length=250)
    address:Optional[str]=Field(default=None,min_length=5,max_length=250)
    contact:Optional[str]=Field(default=None,pattern=r"^(\+91[\-\s]?)?[0]?(91)?[6789]\d{9}$")
    image_url:Optional[str]=None



class CategoryCreate(Validation):
    category_name:str



class CategoryUpdate(BaseModel):
    category_name:Optional[str]

class DishCreate(BaseModel):
    dish_name:str
    price:int

class DishOut(BaseModel):
    dish_name:str
    price:int

class CategoryMenuOut(BaseModel):
    category_name: str
    dishes: List[DishOut]


class RestaurantMenuOut(BaseModel):
    restaurant_name: str
    address: str
    contact: int
    menu: List[CategoryMenuOut]
    image_url:str

