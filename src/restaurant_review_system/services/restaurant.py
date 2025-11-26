from src.restaurant_review_system.repository.restaurant import RestaurantRepo
from sqlalchemy.orm import Session
from src.restaurant_review_system.utils.response import Response
from src.restaurant_review_system.schemas.restaurant import RestaurantUpdate
from fastapi import HTTPException

restaurant_repo=RestaurantRepo()
response=Response()

class RestaurantService:
    def add_restaurant(self,restaurant,fetch_owner_id,db:Session):

            new_restaurant=restaurant_repo.add_restaurant(restaurant,fetch_owner_id,db)

            return {"Msg":"Restaurant created successfully", "restaurant_id": new_restaurant.restaurant_id}

    def add_category(self,restaurant_id,category,db:Session):
            resaturant=restaurant_repo.find_restaurant(restaurant_id,db)
            if not resaturant:
                raise HTTPException(status_code=403,detail="No Such Resaturant")

            new_category=restaurant_repo.add_category(restaurant_id,category,db)

            return {"Msg":"Sucessfully add new Category","Category_id":new_category.category_id}
    
    
    def add_dish(self,category_id,dish,db:Session,owner_id):
          category_fetch=restaurant_repo.find_category(category_id,db)

          if not category_fetch:
                raise HTTPException(status_code=403,detail="No such category available")
          
          restaurant1=category_fetch.restaurantinfo

          if restaurant1.owner_id !=owner_id:
                raise HTTPException(status_code=403,detail="You can only add dishes to your own restaurant")

          new_dish=restaurant_repo.add_dish(category_id,category_fetch,dish,db)

          return {"msg":"Dish Added","dish_id":new_dish.dish_id}
          


    def restaurant_details(self,db:Session,restaurant_id):

            restaurant =restaurant_repo.restaurant_details(db,restaurant_id)

            if not restaurant:
                raise HTTPException(status_code=404, detail="Restaurant not found")

            menu_data = []
            for cat in restaurant.categories:
                dishes_data=[{"dish_name":dish.dish_name,"price":dish.price} for dish in cat.dishes]
                menu_data.append({
                    "category_name": cat.category_name,
                    "dishes": dishes_data
                })

            return {
                "restaurant_name": restaurant.restaurant_name,
                "address": restaurant.address,
                "contact": restaurant.contact,
                "menu": menu_data,
                "image_url":restaurant.image_url
            }
    
    def get_all_restaurants(self,db:Session):
          db_restaurant=restaurant_repo.get_all_restaurants(db)

          return db_restaurant
          

    def get_rating_restaurant(self,restaurant_id,db:Session):

        db_review=restaurant_repo.get_rating_restaurant(restaurant_id,db)
        if not db_review:
              raise HTTPException(status_code=403,detail="No Reviews Yet")
        restaurant_rating=[]
        for row in db_review:
              avg_per_person=round((row.ambience_rating+row.cleanliness_rating+row.food_rating+row.service_rating)/4,1)
              restaurant_rating.append(avg_per_person)
        restaurant_overall_rating=round(sum(restaurant_rating)/len(restaurant_rating),1)
              
        return {
              "restaurant_rating":restaurant_overall_rating
        }

    def get_owner_restaurants(self,owner_id,db:Session):
          db_restaurants=restaurant_repo.get_owner_restaurants(owner_id,db)
          if not db_restaurants:
                raise HTTPException(status_code=403,detail="No Such Restaurant")
          return {
                "my_restaurants":db_restaurants
          }
    
    def all_categories(self,restaurant_id,db:Session):
            db_categories=restaurant_repo.all_categories(restaurant_id,db)

            return{
                "All_Categories":db_categories
            }
    
    def delete_restaurant(self,restaurant_id,db:Session):
          try:
                  
            db_restaurant=restaurant_repo.find_restaurant(restaurant_id,db)
            if not db_restaurant:
                  return response.error_response("No Such Restaruant")
            restaurant_repo.delete(db_restaurant,db)
            return response.sucess_response("Restaurant Deleted Sucessfully")
 
          except Exception as e:
                
                return response.error_response(str(e))
                         
      
    def update_restaurant_details(self,restaurant_id,update_restaurant:RestaurantUpdate,db:Session):
          try:
                
            db_restaruant=restaurant_repo.find_restaurant(restaurant_id,db)
            if not db_restaruant:
                  return response.error_response("No such Restaurant",403)
            
            update_data=update_restaurant.model_dump(exclude_unset=True)
            
            restaurant_repo.update_restaurant_details(db_restaruant,update_data,db)

            return response.sucess_response("Update Restaurant Details")
            

          except Exception as e:
                
                return response.error_response(str(e))
          


    def delete_catgeory(self,restaurant_id,category_id,db):
          db_category=restaurant_repo.delete_category(restaurant_id,category_id,db)
          if not db_category:
                return response.error_response("No such category",403)
          restaurant_repo.delete(db_category,db)
          return response.sucess_response("Deleted Category Sucessfully")
                