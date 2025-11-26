from src.restaurant_review_system.backend.models import Restaurant,Category,Dish,Reviews

from sqlalchemy.orm import Session,joinedload


class RestaurantRepo:

    def add_restaurant(self,restaurant,fetch_owner_id,db:Session):
            new_restaurant=Restaurant(owner_id=fetch_owner_id,restaurant_name=restaurant.restaurant_name,address=restaurant.address,contact=restaurant.contact,image_url=restaurant.image_url)
            db.add(new_restaurant)
            db.commit()
            db.refresh(new_restaurant)
            return new_restaurant

    
    def add_category(self,restaurant_id,category,db:Session,):
            new_category=Category(category_name=category.category_name,restaurant_id=restaurant_id)

            db.add(new_category)
            db.commit()

            return new_category
         

    def find_restaurant(self,restaurant_id,db:Session):
          resaturant=db.query(Restaurant).filter(Restaurant.restaurant_id==restaurant_id).first()

          return resaturant
          
          

    def find_category(self,category_id,db:Session):
          category_fetch=db.query(Category).filter(Category.category_id==category_id).first()

          return category_fetch
          


    def add_dish(self,category_id,category_fetch,dish,db:Session):


            new_dish=Dish(restaurant_id=category_fetch.restaurant_id,
                        category_id=category_id,
                        dish_name=dish.dish_name,
                        price=dish.price)
            
            db.add(new_dish)
            db.commit()
            return new_dish

    def all_categories(self,restaurant_id,db:Session):
            db_categories=db.query(Category).filter(Category.restaurant_id==restaurant_id).all()

            return db_categories
    
    def restaurant_details(self,db:Session,restaurant_id):
            restaurant = (db.query(Restaurant)
            .options(joinedload(Restaurant.categories).joinedload(Category.dishes)).filter(Restaurant.restaurant_id == restaurant_id)
            .first()
            )


            return restaurant

    def get_all_restaurants(self,db:Session):
        db_restaurant=db.query(Restaurant).all()

        return db_restaurant
    


    def get_rating_restaurant(self,restaurant_id,db:Session):

        db_review=db.query(Reviews).filter(Reviews.restaurant_id==restaurant_id).all()

        return db_review
    
    def get_owner_restaurants(self,owner_id,db:Session):
        db_restaurants=db.query(Restaurant).filter(Restaurant.owner_id==owner_id).all()

        return db_restaurants
    def update_restaurant_details(self,update_data,db_restaruant,db:Session):
        for key,value in update_data.items():
                  setattr(db_restaruant,key,value)
 
        db.commit()

    def delete(self,data,db:Session):
          db.delete(data)
          db.commit()
   
    def delete_category(self,restaurant_id,category_id,db:Session):
          db_category=db.query(Category).filter(Category.restaurant_id==restaurant_id,Category.category_id==category_id).first()
          return db_category
      