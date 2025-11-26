from src.restaurant_review_system.repository.reviewer import Reviewer
from sqlalchemy.orm import Session


from fastapi import HTTPException
from src.restaurant_review_system.schemas.reviews import DishReviewCreate,RestaurantReviewCreate
from src.restaurant_review_system.utils.response import Response

from fastapi.encoders import jsonable_encoder
from src.restaurant_review_system.schemas.reviews import MyReviews


reviewer_repo=Reviewer()
response=Response()

class ReviewerService:

    def review_dish(self,review:DishReviewCreate,reviewer_id,db:Session):
         ordered = reviewer_repo.fetch_ordered_dish(review,reviewer_id,db)
         if not ordered:
                raise HTTPException(status_code=403,detail="You can only review dishes you have ordered.")
         
         existing=reviewer_repo.review_dish(review,db,reviewer_id)
         if existing:
                raise HTTPException(
                    status_code=400,
                    detail="You have already reviewed this dish."
                )      
         reviewer_repo.add_dish_Review(review,db)

         dish=reviewer_repo.dish_data(review,db)

         return {
                "message": "Dish reviewed successfully!",
                "dish_name": dish.dish_name,
                "rating": review.rating
            }


    def review_restaurant(self,restaurant_id:int,review: RestaurantReviewCreate,db: Session,reviewer_id_fetched):
                
                ordered=reviewer_repo.review_restaurant(reviewer_id_fetched,db)
                if not ordered:
                    raise HTTPException(status_code=400, detail="User has not ordered any food yet.")
                
                review_already=reviewer_repo.reviewer_data(restaurant_id,reviewer_id_fetched,db)
                if review_already:
                      raise HTTPException(status_code=403,detail="You have already reviewed this restaurant")
                
                reviewer_repo.add_review(restaurant_id,ordered,review,db,reviewer_id_fetched)

                db_restaurant=reviewer_repo.restaurant_details(restaurant_id,db)
                restaurant_name=db_restaurant.restaurant_name
                return{"Sucessfully added review for ":restaurant_name}
        
    def get_all_restaurant__review(self,restaurant_id:int,db:Session):
            db_reviews=reviewer_repo.get_all_restaurant__review(restaurant_id,db)
            if not db_reviews:
                raise HTTPException(status_code=404, detail="No reviews found for this restaurant")
            

            review_list=[]
            for review in db_reviews:
                db_user=reviewer_repo.user_data(review,db)
                avg_rating = round((review.ambience_rating + review.service_rating + review.food_rating + review.cleanliness_rating) / 4, 1)
                review_list.append(
                    {
                        "username":db_user.username,
                        "comment":review.comment,
                        "avg_rating":avg_rating
                    }
                )

            return review_list


    def get_my_reviews(self,reviewer_id,db):
          my_reviews=reviewer_repo.my_all_reviews(reviewer_id,db)
          if not my_reviews:
                return response.error_response("Not Yet Reviewed Restaurant",404)
        
          formatted_reviews = [MyReviews.model_validate(review).model_dump() for review in my_reviews]

          return response.sucess_response(formatted_reviews)
        #   return my_reviews

    def delete_review(self,reviewer_id,restaurant_id,db:Session):
          db_review=reviewer_repo.my_review(db,reviewer_id,restaurant_id)
          if not db_review:
                return  response.error_response("No such review of this user")
          db.delete(db_review)
          db.commit()

          return response.sucess_response("Review Deleted Sucessfully")
          
          
          
          

          
          
    