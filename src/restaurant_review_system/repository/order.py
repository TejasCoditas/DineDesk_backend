from src.restaurant_review_system.backend.models import OrderedFood,Dish,DishReview,Restaurant
from sqlalchemy.orm import Session
from src.restaurant_review_system.schemas.orders import OrderItem




class Order:
    def get_all_restaurant_dishes(self,restaurant_id:int,db:Session):
        db_food=db.query(Dish).filter(Dish.restaurant_id==restaurant_id).all()
        return db_food

    def place_order(self,order_data: OrderItem,db: Session):
            
            dish = db.query(Dish).filter(Dish.dish_id == order_data.dish_id).first()

            return dish
    
    def existing_dish(self,order_data: OrderItem,reviewer_id,db:Session):
         existing = (db.query(DishReview).filter(DishReview.dish_id == order_data.dish_id,DishReview.reviewer_id == reviewer_id).first())

         return existing
    
    def all_order_history(self,customer_id,db:Session):

        db_orders=db.query(OrderedFood).filter(OrderedFood.reviewer_id==customer_id).all()

        return db_orders
         
    def revenue_restaurant(self,restaurant_id,db:Session):

            dish_ids=db.query(Dish.dish_id).filter(Dish.restaurant_id==restaurant_id).all()

            return dish_ids
    
    def dish_data(self,order,db:Session):
          dish_data=db.query(Dish).filter(Dish.dish_id==order.dish_id).first()
          return dish_data
          
    
    def order_prices(self,dish,db:Session):
         order_prices=db.query(OrderedFood.price).filter(OrderedFood.dish_id==dish).all()

         return order_prices
         
    
    def all_restaurant_revenue(self,db:Session):

            restaurants = db.query(Restaurant).all()

            return restaurants
    
    def add_order_details(self,order_data,reviewer_id,subtotal,db:Session):
         new_order= OrderedFood(
            reviewer_id=reviewer_id,
            dish_id=order_data.dish_id,
            quantity=order_data.quantity,
            price=subtotal
        )
         db.add(new_order)

    def add_dish_review(self,reviewer_id,order_data,db:Session):
        new_review = DishReview(reviewer_id=reviewer_id,dish_id=order_data.dish_id,rating=order_data.dish_rating)

        db.add(new_review)
        db.commit()         
          
          