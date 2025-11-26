from pydantic import BaseModel,Field
from src.restaurant_review_system.utils.validation import Validation

class OrderItem(Validation):
    dish_id: int
    quantity: int=Field(ge=1)
    dish_rating:int=Field(ge=0,le=5)


class OrderedDishOut(Validation):
    dish_name: str
    quantity: int
    subtotal: int

class OrderResponse(BaseModel):
    message: str
    total_amount: int
    ordered_items: str
    rating:int


