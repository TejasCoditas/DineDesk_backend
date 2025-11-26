
from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship
from src.restaurant_review_system.backend.config import Base



class User(Base):

    __tablename__="users"

    user_id=Column(Integer,primary_key=True)
    username=Column(String,nullable=False)
    password=Column(String,nullable=False)
    role=Column(String,nullable=False)

    restaurants=relationship("Restaurant",back_populates="owner")

    reviewerorder=relationship("OrderedFood",back_populates="reviewerinfo")

    reviewdish=relationship("DishReview",back_populates="dishreview")

    reviewerdetails=relationship("Reviews",back_populates="reviewerinfo")

class Restaurant(Base):
    __tablename__="restaurants"

    restaurant_id=Column(Integer,primary_key=True)
    owner_id=Column(Integer,ForeignKey("users.user_id"))
    restaurant_name=Column(String,nullable=False)
    address=Column(String,nullable=False)
    contact=Column(String,nullable=False)
    image_url=Column(String,nullable=True)

    owner=relationship("User",back_populates="restaurants")

    categories=relationship("Category",back_populates="restaurantinfo")

    dishs=relationship("Dish",back_populates="restaurantdish")

    reviewerdetails=relationship("Reviews",back_populates="rest_info")

class Category(Base):

    __tablename__="categories"

    category_id=Column(Integer,primary_key=True)
    restaurant_id=Column(Integer,ForeignKey("restaurants.restaurant_id"))
    category_name=Column(String,nullable=False)
    
    restaurantinfo=relationship("Restaurant",back_populates="categories")

    dishes=relationship("Dish",back_populates="categorydish")

class Dish(Base):

    __tablename__="dishes"

    dish_id=Column(Integer,primary_key=True)
    restaurant_id=Column(Integer,ForeignKey("restaurants.restaurant_id"))
    category_id=Column(Integer,ForeignKey("categories.category_id"))
    dish_name=Column(String,nullable=True)
    price=Column(Integer,nullable=False)

    categorydish=relationship("Category",back_populates="dishes")

    restaurantdish=relationship("Restaurant",back_populates="dishs")
    reviewerorder=relationship("OrderedFood",back_populates="reviewerdish")

    dishreview=relationship("DishReview",back_populates="dishdetails")

class OrderedFood(Base):
    __tablename__="orderedfoods"

    order_id=Column(Integer,primary_key=True)
    reviewer_id=Column(Integer,ForeignKey("users.user_id"))
    dish_id=Column(Integer,ForeignKey("dishes.dish_id"))
    quantity=Column(Integer,nullable=False)
    price=Column(Integer,nullable=False)

    reviewerinfo=relationship("User",back_populates="reviewerorder")
    reviewerdish=relationship("Dish",back_populates="reviewerorder")

    reviewerdetails=relationship("Reviews",back_populates="orderinfo")

    

class Reviews(Base):

    __tablename__="reviews"

    review_id=Column(Integer,primary_key=True)
    reviewer_id=Column(Integer,ForeignKey("users.user_id"))
    restaurant_id=Column(Integer,ForeignKey("restaurants.restaurant_id"))
    order_id=Column(Integer,ForeignKey("orderedfoods.order_id"))
    ambience_rating=Column(Integer,nullable=False)
    service_rating=Column(Integer,nullable=False)
    food_rating=Column(Integer,nullable=False)
    cleanliness_rating=Column(Integer,nullable=False)
    comment=Column(String,nullable=False)


    reviewerinfo=relationship("User",back_populates="reviewerdetails")

    rest_info=relationship("Restaurant",back_populates="reviewerdetails")

    orderinfo=relationship("OrderedFood",back_populates="reviewerdetails")




class DishReview(Base):
    __tablename__="dishreviews"

    dishreview_id=Column(Integer,primary_key=True)
    reviewer_id=Column(Integer,ForeignKey("users.user_id"))
    dish_id=Column(Integer,ForeignKey("dishes.dish_id"))   
    rating=Column(Integer,nullable=False)

    dishreview=relationship("User",back_populates="reviewdish")

    dishdetails=relationship("Dish",back_populates="dishreview")










