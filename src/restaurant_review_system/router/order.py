
from src.restaurant_review_system.backend.config import get_db
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session
from src.restaurant_review_system.schemas.orders import OrderResponse,OrderItem
from src.restaurant_review_system.authorization.auth import validate_token
from fastapi import Depends

from src.restaurant_review_system.services.orders import OrderService

orderservice=OrderService()
router = APIRouter(prefix="/order",tags=["FoodOrder"])

@router.get("/all_dishes")
async def all_dishes(restaurant_id:int,db:Session=Depends(get_db)):
    restaurant_dishes=orderservice.get_all_restaurant_dishes(restaurant_id,db)
    return restaurant_dishes

@router.post("/place_order", response_model=OrderResponse)
async def place_order(order_data: OrderItem,db: Session = Depends(get_db),payload: dict = Depends(validate_token(["admin","owner","customer"]))):
    reviewer_id = int(payload.get("sub"))
    place_order=orderservice.place_order(order_data,db,reviewer_id)
    return place_order

    
@router.get("/all_order_history")
async def all_orders_user(db:Session=Depends(get_db),payload: dict = Depends(validate_token(["admin","owner","customer"]))):
    customer_id=int(payload.get("sub"))
    order_history=orderservice.all_order_history(customer_id,db)
    return order_history


@router.get("/revenue_restaurant")
async def revenue_restaurant(restaurant_id:int,db:Session=Depends(get_db)):
    revenue_details=orderservice.revenue_restaurant(restaurant_id,db)
    return revenue_details


@router.get("/all_restaurant_revenue")
async def all_restaurant_revenue(db: Session = Depends(get_db)):
    all_details=orderservice.all_restaurant_revenue(db)
    return all_details




