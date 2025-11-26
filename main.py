from src.restaurant_review_system.router import signin
from src.restaurant_review_system.router import restaurant,order,reviewer
from fastapi import FastAPI,Request
from src.restaurant_review_system.utils.response import Response
from fastapi.exceptions import RequestValidationError
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(signin.router, prefix="/api")
app.include_router(restaurant.router, prefix="/api")
app.include_router(order.router, prefix="/api")
app.include_router(reviewer.router, prefix="/api")

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


lambda_handler=Mangum(app)
response= Response()
import uvicorn

def run():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

    # poetry run start


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request:Request,exc:RequestValidationError):
    error_msgs=[]
    for err in exc.errors():
        msg=err.get("msg","")
        location=err.get("loc")
        error_msgs.append({
            "location":location,
            "msg":msg
        })

    return response.error_response(error_msgs,status_code=422)
