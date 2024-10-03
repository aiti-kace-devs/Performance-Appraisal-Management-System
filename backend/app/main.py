from fastapi.middleware.cors import CORSMiddleware
from db.session import SessionLocal
from fastapi.responses import JSONResponse
import json
from fastapi.exceptions import RequestValidationError
from apis.routers import router as api_router
from config.settings import Settings
from db.init_db import init_db,create_super_admin
from fastapi import FastAPI,Request,status, HTTPException
import uvicorn
from db.init_models import create_tables
from domains.appraisal.schemas.appraisal_section import validate_appraisal_cycles_id
from crud.base import validate_name_uniqueness



## adding our api routes 
def include(app):
    app.include_router(api_router)



def initial_data_insert():
   
    db = SessionLocal()
    try:
        init_db(db)
        create_super_admin(db)
    finally:
        db.close()


    


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
    #create_tables()
    initial_data_insert()
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
    if request.method == "POST":
        path = request.url.path
        
        # Apply validation only if the path contains 'appraisal_configurations' or 'appraisal_sections'
        if "appraisal_configurations" in path or "appraisal_sections" in path:
            body = await request.body()
            body_str = body.decode('utf-8')
            try:
                data = json.loads(body_str)
                
                if "appraisal_configurations" in path:
                    if "configuration" in data:
                        config_value = data["configuration"]
                        if isinstance(config_value, dict):
                            try:
                                json_str = json.dumps(config_value)
                                json.loads(json_str)  # Validate if it is valid JSON
                            except (TypeError, json.JSONDecodeError):
                                raise HTTPException(status_code=400, detail="Configuration must be a valid JSON object")
                        else:
                            raise HTTPException(status_code=400, detail="Configuration must be a dictionary containing valid JSON data")
                    else:
                        raise HTTPException(status_code=422, detail="Configuration field is missing in the request body")
                
                if "appraisal_sections" in path:
                    if "appraisal_cycles_id" in data:
                        db = SessionLocal()
                        response = validate_appraisal_cycles_id(data["appraisal_cycles_id"], db)
                    else:
                        raise HTTPException(status_code=422, detail="appraisal_cycles_id field is missing in the request body")
                
                # Validate name uniqueness for AppraisalCycle and AppraisalSection
                model_name = None
                if "appraisal_cycles" in path:
                    model_name = 'AppraisalCycle'
                elif "appraisal_sections" in path:
                    model_name = 'AppraisalSection'
                
                if model_name and "name" in data:
                    db = SessionLocal()
                    if not validate_name_uniqueness(model_name, data["name"], db):
                        raise HTTPException(status_code=400, detail=f"{model_name} column 'name' already exists")
                    db.close()
            
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        else:
            # Print a message if the path does not match the intended models
            print(f"Unintended path: {path}\n NOT intended for this model")
    
    response = await call_next(request)
    return response



@app.exception_handler(json.JSONDecodeError)
async def json_decode_error_handler(request: Request, exc: json.JSONDecodeError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Configuration must be a valid JSON object"},
    )



from fastapi import Request, HTTPException, Depends
import requests
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
import os
from db.session import get_db
from datetime import datetime
from domains.auth.models.users import User
from config.settings import settings


class IntruderDetectionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, db: Session = Depends(get_db)):
        super().__init__(app)
        self.db = db
    
    async def intruder_info(request: Request):
        #intruder_list = []
        client_ip = request.client.host
        headers = request.headers
        user_agent = headers.get("User-Agent")
        mac_address = headers.get("X-MAC-Address")  # Custom header for MAC Address
        location = requests.get(f"https://ipinfo.io/{client_ip}/geo").json()

        intruder_info = {
            "ip_address": client_ip,
            "mac_address": mac_address,
            "user_agent": user_agent,
            "location": location,
        }
        print("intruder info dict: ", intruder_info)
        settings.intruder_list.append(intruder_info)
        print(f"Intruder detected: {intruder_info}")

        return intruder_info


    async def log_intruder_info(ip_addr: str, mac_addr: str, user_agent: str, location: str):
        # Get current date to create or append to the log file
        current_date = datetime.now().strftime('%Y-%m-%d')
        log_file_name = f"intruder_log_{current_date}.txt"
        log_directory = "security/logs/"

        os.makedirs(log_directory, exist_ok=True)
        

        # Check if the log file exists
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        
        log_filepath = os.path.join(log_directory, log_file_name)
        

        # Create log entry
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{ip_addr} | {mac_addr} | {user_agent} | {location} | {timestamp}"

        # Check if the log file already exists
        if os.path.exists(log_filepath):
            with open(log_filepath, 'a') as file:
                file.write("================================================================================\n")
                file.write(log_entry + "\n")
        else:
            with open(log_file_name, 'w') as file:
                file.write("IP Addr | Mac Addr | User Agent | location | Timestamp\n")
                file.write(log_entry + "\n")

        return log_filepath

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        print("response in middleware: ", response)
        # Example of handling rate limit exceeded and locking accounts
        if response.status_code == 429:  # Too Many Requests
            username = request.headers.get("X-Username")
            print("\nusername in middleware: ", username)
            if username:
                user = self.db.query(User).filter(User.username == username).first()
                if user:
                    print("user in middleware: ", user)
                    user.lock_account(lock_time_minutes=10)
                    self.db.commit()
                    # info = await IntruderDetectionMiddleware.intruder_info(request=request)
                    # log = await IntruderDetectionMiddleware.log_intruder_info(info.get('ip_address'), info.get('mac_address'), info.get('user_agent'), info.get('location'))

                    # print("log info: ", log)


        return response

#app.middleware("http")(IntruderDetectionMiddleware())
app.add_middleware(IntruderDetectionMiddleware)



if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8080, log_level="info", reload = True)
    print("running")