from src.restaurant_review_system.repository.order import Order


from sqlalchemy.orm import Session
from src.restaurant_review_system.schemas.orders import OrderItem
from fastapi import HTTPException



order_repo=Order()


class OrderService:

    def get_all_restaurant_dishes(self,restaurant_id:int,db:Session):
        food=order_repo.get_all_restaurant_dishes(restaurant_id,db)
        if not food:
            raise HTTPException(status_code=403,detail="No Such Restaurant ")
        
        dishes_list=[{"dish_id":row.dish_id,"dish_name":row.dish_name} for row in food]

        return dishes_list

    def place_order(self,order_data: OrderItem,db: Session,reviewer_id):
        total_amount=0
        dish=order_repo.place_order(order_data,db)

        if not dish:
                raise HTTPException(status_code=404, detail=f"Dish ID not found")

        subtotal = dish.price * order_data.quantity
        total_amount += subtotal

        order_repo.add_order_details(order_data,reviewer_id,subtotal,db)

        existing=order_repo.existing_dish(order_data,reviewer_id,db)
        if existing:
                raise HTTPException(status_code=400,detail="You have already reviewed this dish.")

        order_repo.add_dish_review(reviewer_id,order_data,db)

        return {
                "message": "Order Added and Reviewed successfully ",
                "total_amount": total_amount,
                "ordered_items": dish.dish_name,
                "rating":order_data.dish_rating
            }




    def all_order_history(self,customer_id:int,db:Session):
        order_list=[]
        db_orders=order_repo.all_order_history(customer_id,db)

        if not db_orders:
            raise HTTPException(status_code=404,detail="No customer data available")
        
        for order in db_orders:
            dish_data=order_repo.dish_data(order,db)
            order_list
            order_list.append(dish_data.dish_name)
             
        return{
            "orders":order_list
        }



    def revenue_restaurant(self,restaurant_id:int,db:Session):
        dish_ids=order_repo.revenue_restaurant(restaurant_id,db)
        total_revenue=0
        total_prices=[]
        if not dish_ids:
            raise HTTPException(status_code=404,detail="No dishes for This restaurant")
            
        dish_id=[d[0]for d in dish_ids]
    
        for dish in dish_id:
            user_prices=order_repo.order_prices(dish,db)
            ordered_dishes_prices=[dish[0]for dish in user_prices]

            total_prices.extend(ordered_dishes_prices)

        total_revenue= sum(total_prices)
        
        return {
            "Details":total_revenue
        }
    

    def all_restaurant_revenue(self,db:Session):
        restaurants=order_repo.all_restaurant_revenue(db)

        if not restaurants:
            raise HTTPException(status_code=404, detail="No restaurants found")


        all_revenues = []
        for rest in restaurants:
            
            total_prices = []

            dish_ids = order_repo.revenue_restaurant(rest.restaurant_id,db)


            dish_id_list = [dish[0] for dish in dish_ids]


            for dish_id in dish_id_list:
                orders =order_repo.order_prices(dish_id,db)
                total_prices.extend([order[0] for order in orders if order is not None])

            total_revenue = sum(total_prices)

            all_revenues.append({
                "restaurant_name": rest.restaurant_name,
                "restaurant_id": rest.restaurant_id,
                "total_revenue": total_revenue
            })

        return {"restaurants": all_revenues}
