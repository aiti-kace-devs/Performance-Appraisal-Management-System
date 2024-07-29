from fastapi.middleware.cors import CORSMiddleware
from db.session import SessionLocal
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from apis.routers import router as api_router
from config.settings import Settings
from db.init_db import init_db
from fastapi import FastAPI,Request,status
import uvicorn
from db.init_models import create_tables



## adding our api routes 
def include(app):
    app.include_router(api_router)



def initial_data_insert():

    db = SessionLocal()
    init_db(db)


    


def start_application():
    app = FastAPI(docs_url="/", title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)
    app.add_middleware(
    CORSMiddleware,
    allow_origins= Settings.SET_NEW_ORIGIN,
    allow_credentials=True,    
    allow_methods=["*"],
    allow_headers=["*"]
    )
    #initial_data_insert()
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




if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8080, log_level="info", reload = True)
    print("running")