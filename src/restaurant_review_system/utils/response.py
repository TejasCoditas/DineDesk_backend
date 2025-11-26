from fastapi.responses import JSONResponse

class Response:
    def sucess_response(self,data):
        return JSONResponse(
            content={
                "data":data,
                "error":"Null"
            },
            status_code=200
        )
    
    def error_response(self,error_msg,status_code=400):
        return JSONResponse(
            content={
                "data":"Null",
                "error":error_msg
            },
            status_code=status_code
        )