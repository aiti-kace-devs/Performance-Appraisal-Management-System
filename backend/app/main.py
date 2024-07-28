from fastapi.middleware.cors import CORSMiddleware
from db.session import SessionLocal
from fastapi.responses import JSONResponse
import json
from fastapi.exceptions import RequestValidationError
from apis.routers import router as api_router
from config.settings import Settings
from db.init_db import init_db
from fastapi import FastAPI,Request,status, HTTPException
import uvicorn
from db.init_models import create_tables




## adding our api routes 
def include(app):
    app.include_router(api_router)



def initial_data_insert():
    try:
        db = SessionLocal()
        init_db(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



    


def start_application():
    app = FastAPI(docs_url="/", title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)
    app.add_middleware(
    CORSMiddleware,
    allow_origins= Settings.SET_NEW_ORIGIN,
    allow_credentials=True,    
    allow_methods=["*"],
    allow_headers=["*"]
    )
    include(app)
    create_tables()
    return app
app = start_application()




# Custom error handling middleware
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_message = "Validation error occurred"
    # Optionally, you can log the error or perform additional actions here
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": error_message+f"{exc}"})



# Generic error handler for all other exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    error_message = "An unexpected error occurred:\n"
    # Optionally, you can log the error or perform additional actions here
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": error_message+f"{exc}"})


@app.middleware("http")
async def validate_configuration_middleware(request: Request, call_next):
    if request.method in ["POST", "PUT"]:
        body = await request.body()
        body_str = body.decode('utf-8')

        try:
            data = json.loads(body_str)
        except json.JSONDecodeError as e:
            #print(f"JSONDecodeError: {str(e)} - body_str: {body_str}")
            raise HTTPException(status_code=400, detail="Request body must be valid JSON")

        if "configuration" in data:
            config_value = data["configuration"]
            if isinstance(config_value, dict):
                try:
                    json_str = json.dumps(config_value)
                    json.loads(json_str)  # Validate if it is valid JSON
                except (TypeError, json.JSONDecodeError) as e:
                    #print(f"Invalid JSON in configuration: {str(e)} - config_value: {config_value}")
                    raise HTTPException(status_code=400, detail="Configuration must be a valid JSON object")
            else:
                #print(f"Invalid configuration type: {type(config_value)} - config_value: {config_value}")
                raise HTTPException(status_code=400, detail="Configuration must be a dictionary containing valid JSON data")
        else:
            #print("Configuration field is missing in the request body")
            raise HTTPException(status_code=422, detail="Configuration field is missing in the request body")
                
    response = await call_next(request)
    return response




@app.exception_handler(json.JSONDecodeError)
async def json_decode_error_handler(request: Request, exc: json.JSONDecodeError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Configuration must be a valid JSON object"},
    )


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8080, log_level="info", reload = True)
    print("running")