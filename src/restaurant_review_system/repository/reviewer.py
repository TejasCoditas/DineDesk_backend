from src.restaurant_review_system.backend.models import Dish,OrderedFood,DishReview,Restaurant,Reviews,User
from sqlalchemy.orm import Session
from src.restaurant_review_system.schemas.reviews import DishReviewCreate,RestaurantReviewCreate


class Reviewer:

    def fetch_ordered_dish(self,review:DishReviewCreate,reviewer_id,db:Session):
         ordered = db.query(OrderedFood).filter(OrderedFood.dish_id == review.dish_id,OrderedFood.reviewer_id == reviewer_id).first()

         return ordered
         
            

    def review_dish(self,review: DishReviewCreate,db: Session,reviewer_id):

            existing = (db.query(DishReview).filter(DishReview.dish_id == review.dish_id,DishReview.reviewer_id == reviewer_id).first())

            return existing

    def add_dish_Review(self,review: DishReviewCreate,db: Session,reviewer_id):
            new_review = DishReview(reviewer_id=reviewer_id,dish_id=review.dish_id,rating=review.rating)

            db.add(new_review)
            db.commit()

            return new_review

    def dish_data(self,review:DishReviewCreate,db:Session):
          dish = db.query(Dish).filter(Dish.dish_id == review.dish_id).first()
          return dish
          


    def reviewer_data(self,restaurant_id,reviewer_id:int,db:Session):
           reviewer_data=db.query(Reviews).filter(Reviews.restaurant_id==restaurant_id,Reviews.reviewer_id==reviewer_id).first()
           return reviewer_data
        
    

    def review_restaurant(self,reviewer_id_fetched,db: Session):
            
            ordered=db.query(OrderedFood).filter(OrderedFood.reviewer_id==reviewer_id_fetched).first()
            return ordered

    
    def restaurant_details(self,restaurant_id,db:Session):
            resturant_name=db.query(Restaurant.restaurant_name).filter(Restaurant.restaurant_id==restaurant_id).first()
            return resturant_name
          
    def add_review(self,restaurant_id:int,ordered,review: RestaurantReviewCreate,db: Session,reviewer_id_fetched):
            new_review=Reviews(
                reviewer_id=reviewer_id_fetched,
                restaurant_id=restaurant_id,
                order_id=ordered.order_id,
                ambience_rating=review.ambience_rating,
                service_rating=review.service_rating,
                food_rating=review.food_rating,
                cleanliness_rating=review.cleanliness_rating,
                comment=review.comment
            )
            db.add(new_review)
            db.commit()       
          

    def get_all_restaurant__review(self,restaurant_id:int,db:Session):
            db_reviews=db.query(Reviews).filter(Reviews.restaurant_id==restaurant_id).all()

            return db_reviews
    
    def user_data(self,review,db:Session):
          db_user=db.query(User).filter(User.user_id==review.reviewer_id).first()
          return db_user
          
    
    def my_all_reviews(self,reviewer_id,db:Session):
           my_reviews=db.query(Reviews).filter(Reviews.reviewer_id==reviewer_id).all()
           return my_reviews
    
    def my_review(self,db:Session,reviewer_id=None,restaurant_id=None):
           if reviewer_id and restaurant_id: 
                my_review_restaurant=db.query(Reviews).filter(Reviews.restaurant_id==restaurant_id,Reviews.reviewer_id==reviewer_id).first()
                return my_review_restaurant
        