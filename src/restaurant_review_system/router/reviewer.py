from src.restaurant_review_system.backend.config import get_db
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session
from src.restaurant_review_system.authorization.auth import validate_token
from fastapi import Depends
from src.restaurant_review_system.schemas.reviews import DishReviewCreate,RestaurantReviewCreate,AllReviews,MyReviews
from typing import List
from src.restaurant_review_system.services.reviewer import ReviewerService
from src.restaurant_review_system.utils.response import Response



router=APIRouter(prefix="/customer",tags=["Reviewer"])
response=Response()

reviewer_service=ReviewerService()

@router.post("/review_dish")
async def review_dish(review: DishReviewCreate,db: Session = Depends(get_db),payload: dict = Depends(validate_token(["owner", "admin", "customer"]))):

    reviewer_id = int(payload.get("sub"))
    review_info=reviewer_service.review_dish(review,reviewer_id,db)
    return review_info


@router.post("/review_restaurant")
async def review_restaurant(restaurant_id:int,review: RestaurantReviewCreate,db: Session = Depends(get_db),payload: dict = Depends(validate_token(["customer", "owner", "admin"]))):
    reviewer_id_fetched = int(payload.get("sub"))
    restaurant_name=reviewer_service.review_restaurant(restaurant_id,review,db,reviewer_id_fetched)

    return restaurant_name


@router.get("/all_reviews",response_model=List[AllReviews])
async def get_reviews(restaurant_id:int,db:Session=Depends(get_db)):
    review_list=reviewer_service.get_all_restaurant__review(restaurant_id,db)
    return review_list


    
@router.get("/get_my_reviews")
async def get_my_reviews(reviewer_id:int,db:Session=Depends(get_db)):

    reviewer_reviews=reviewer_service.get_my_reviews(reviewer_id,db)

    return reviewer_reviews

@router.delete("/delete/myreview")
async def delete_my_review(reviewer_id,restaurant_id,db:Session=Depends(get_db)):
    db_review=reviewer_service.delete_review(reviewer_id,restaurant_id,db)
    return db_review

