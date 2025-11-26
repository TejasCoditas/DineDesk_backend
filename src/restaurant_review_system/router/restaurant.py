from src.restaurant_review_system.backend.config import get_db
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session
from src.restaurant_review_system.schemas.restaurant import DishCreate,RestaurantCreate,CategoryCreate,RestaurantMenuOut,RestaurantUpdate,CategoryUpdate
from src.restaurant_review_system.authorization.auth import validate_token
from fastapi import Depends

from src.restaurant_review_system.services.restaurant import RestaurantService



restaurant_service=RestaurantService()

router=APIRouter(tags=["Restaurant"])

@router.post("/add_restaurant")
async def create_restaurant(restaurant:RestaurantCreate,db:Session=Depends(get_db),payload:dict=Depends(validate_token(["owner","admin"]))):
    fetch_owner_id=int(payload.get("sub"))

    new_restaurant=restaurant_service.add_restaurant(restaurant,fetch_owner_id,db)
    return new_restaurant

@router.patch("/update_restaurant_details")
async def update_restaurant_details(restaurant_id:int,update_restaurant:RestaurantUpdate,db:Session=Depends(get_db)):
    db_restaurant=restaurant_service.update_restaurant_details(restaurant_id,update_restaurant,db)
    return db_restaurant


@router.delete("/delete_restaurant")
async def delete_restaurant(restaurant_id:int,db:Session=Depends(get_db)):
    db_restaurant=restaurant_service.delete_restaurant(restaurant_id,db)
    return db_restaurant



@router.post("/add_category")
async def add_category(restaurant_id:int,category:CategoryCreate,db:Session=Depends(get_db),payload:dict=Depends(validate_token(["owner","admin"]))):
    added_category=restaurant_service.add_category(restaurant_id,category,db)
    return added_category

@router.patch("/update_category")
async def update_category(restaurant_id:int,update_category:CategoryUpdate,db:Session=Depends(get_db)):
    # db_category
    pass

@router.delete("/delete_category")
async def delete_catgeory(restaurant_id:int,category_id:int,db:Session=Depends(get_db)):
    db_category=restaurant_service.delete_catgeory(restaurant_id,category_id,db)
    return db_category






@router.get("/all_categories")
async def get_all_categories(restaurant_id:int,db:Session=Depends(get_db)):
    all_categories=restaurant_service.all_categories(restaurant_id,db)
    return all_categories


@router.post("/add_dishes")
async def add_dish(category_id:int,dish:DishCreate,db:Session=Depends(get_db),payload:dict=Depends(validate_token(["owner","admin"]))):
    owner_id=int(payload.get("sub"))
    added_dish=restaurant_service.add_dish(category_id,dish,db,owner_id)
    return added_dish


@router.get("/restaurants/{restaurant_id}", response_model=RestaurantMenuOut)
async def get_restaurant_menu(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant_details=restaurant_service.restaurant_details(db,restaurant_id)
    return restaurant_details


@router.get("/all_restaurants")
async def get_all_restaurants(db:Session=Depends(get_db)):
    all_restaurants=restaurant_service.get_all_restaurants(db)

    return all_restaurants

@router.get("/restaurant_avg_rating")
async def get_avg_restaurant_rating(restaurant_id:int,db:Session=Depends(get_db)):
    restaurant_rating=restaurant_service.get_rating_restaurant(restaurant_id,db)
    return restaurant_rating

@router.get("/owner_restaurants")
async def owner_restaurants(db:Session=Depends(get_db),payload:dict=Depends(validate_token(["owner","admin"]))):
    owner_id=int(payload.get("sub"))
    all_restaurants=restaurant_service.get_owner_restaurants(owner_id,db)
    return all_restaurants

