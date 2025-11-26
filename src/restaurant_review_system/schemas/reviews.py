from pydantic import BaseModel


class DishReviewCreate(BaseModel):
    dish_id: int
    rating: int  


class RestaurantReviewCreate(BaseModel):
    
    ambience_rating: float
    cleanliness_rating: int
    comment: str
    food_rating: int
    service_rating: int

class AllReviews(BaseModel):
    username:str
    comment:str
    avg_rating:float

class RestaurantName(BaseModel):
    restaurant_name:str
    
    class Config:
        from_attributes = True

class MyReviews(BaseModel):
    restaurant_id:int
    ambience_rating:int
    service_rating:int
    food_rating:int
    cleanliness_rating:int
    comment:str
    rest_info:RestaurantName

    class Config:
        from_attributes = True

#     comment:str