from fastapi.middleware.cors import CORSMiddleware
from db.session import SessionLocal
from fastapi.responses import JSONResponse
import json
from fastapi.exceptions import RequestValidationError
from apis.routers import router as api_router
from config.settings import Settings
from db.init_db import init_db
from fastapi import FastAPI,Request,status, HTTPException, Response
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
    #initial_data_insert()
    include(app)
    create_tables()
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


# @app.middleware("http")
# async def validate_configuration_middleware(request: Request, call_next):
#     if request.method in ["POST"]:
#         path = request.url.path
#         body = await request.body()
#         body_str = body.decode('utf-8')
#         try:
#             data = json.loads(body_str)
#             if "appraisal_configurations" in path:
#                 if "configuration" in data:
#                     config_value = data["configuration"]
#                     if isinstance(config_value, dict):
#                         try:
#                             json_str = json.dumps(config_value)
#                             json.loads(json_str)  # Validate if it is valid JSON
#                         except (TypeError, json.JSONDecodeError):
#                             raise HTTPException(status_code=400, detail="Configuration must be a valid JSON object")
#                     else:
#                         raise HTTPException(status_code=400, detail="Configuration must be a dictionary containing valid JSON data")
#                 else:
#                     raise HTTPException(status_code=422, detail="Configuration field is missing in the request body")
#             elif "appraisal_sections" in path:
#                 if "appraisal_cycles_id" in data:
#                     db = SessionLocal()
#                     response = validate_appraisal_cycles_id(data["appraisal_cycles_id"], db)
#                 else:
#                     raise HTTPException(status_code=422, detail="appraisal_cycles_id field is missing in the request body")
#             # Validate name uniqueness for AppraisalCycle and AppraisalSection
#             model_name = None
#             if "appraisal_cycles" in path:
#                 model_name = 'AppraisalCycle'
#             elif "appraisal_sections" in path:
#                 model_name = 'AppraisalSection'
            
#             if model_name and "name" in data:
#                 db = SessionLocal()
#                 if not validate_name_uniqueness(model_name, data["name"], db):
#                     raise HTTPException(status_code=400, detail=f"{model_name} column 'name' already exist")
#                 db.close()
#         except Exception as e:
#             selected_models = ["appraisal_configurations", "appraisal_sections"]
#             if path in selected_models:
#                 raise HTTPException(status_code=400, detail=str(e))
            
#             print(f"Unintended Exception: {e}\n NOT intended for this model")
    
#     response = await call_next(request)
#     return response


# @app.middleware("http")
# async def validate_configuration_middleware(request: Request, call_next):
#     if request.method in ["POST", "PUT"]:
#         path = request.url.path
#         if "appraisal_configurations" in path:
#             body = await request.body()
#             body_str = body.decode('utf-8')
#             try:
#                 data = json.loads(body_str)
#                 if "configuration" in data:
#                     config_value = data["configuration"]
#                     if isinstance(config_value, dict):
#                         try:
#                             json_str = json.dumps(config_value)
#                             json.loads(json_str)  # Validate if it is valid JSON
#                         except (TypeError, json.JSONDecodeError):
#                             raise HTTPException(status_code=400, detail="Configuration must be a valid JSON object")
#                     else:
#                         raise HTTPException(status_code=400, detail="Configuration must be a dictionary containing valid JSON data")
#                 else:
#                     raise HTTPException(status_code=422, detail="Configuration field is missing in the request body")
#             except json.JSONDecodeError:
#                 raise HTTPException(status_code=400, detail="Request body must be valid JSON")
#         elif "appraisal_sections" in path:
#             body = await request.body()
#             body_str = body.decode('utf-8')
#             try:
#                 data = json.loads(body_str)
#                 if "appraisal_cycles_id" in data:
#                     db = SessionLocal()
#                     response = validate_appraisal_cycles_id(data["appraisal_cycles_id"], db)
#                 else:
#                     raise HTTPException(status_code=422, detail="appraisal_cycles_id field is missing in the request body")
#             except Exception as e:
#                 raise HTTPException(status_code=400, detail=str(e))
#         # Pass for other models
#     response = await call_next(request)
#     return response


# @app.middleware("http")
# async def validate_configuration_middleware(request: Request, call_next):
#     if request.method in ["POST", "PUT"]:
#         body = await request.body()
#         body_str = body.decode('utf-8')
#         print("body_str: ", body_str)
#         print("isinstance: ", isinstance(body_str, str))
#         try:
#             data = json.loads(body_str)
#             if "configuration" in body_str:
#                 data = json.loads(body_str)
#                 print("data: ", data)
#                 if "configuration" in data:
#                     config_value = data["configuration"]
#                     if isinstance(config_value, dict):
#                         try:
#                             json_str = json.dumps(config_value)
#                             json.loads(json_str)  # Validate if it is valid JSON
#                         except (TypeError, json.JSONDecodeError) as e:
#                             #print(f"Invalid JSON in configuration: {str(e)} - config_value: {config_value}")
#                             raise HTTPException(status_code=400, detail="Configuration must be a valid JSON object")
#                     else:
#                         #print(f"Invalid configuration type: {type(config_value)} - config_value: {config_value}")
#                         raise HTTPException(status_code=400, detail="Configuration must be a dictionary containing valid JSON data")
#                 else:
#                     #print("Configuration field is missing in the request body")
#                     raise HTTPException(status_code=422, detail="Configuration field is missing in the request body")
#             else:
#                 db = SessionLocal()
#                 print("appraisal_cycles_id: ", data["appraisal_cycles_id"])
#                 response = validate_appraisal_cycles_id(data["appraisal_cycles_id"],db)
#                 print("response: ",response)
#         except json.JSONDecodeError as e:
#             #print(f"JSONDecodeError: {str(e)} - body_str: {body_str}")
#             raise HTTPException(status_code=400, detail="Request body must be valid JSON")
         
#     response = await call_next(request)
#     return response




@app.exception_handler(json.JSONDecodeError)
async def json_decode_error_handler(request: Request, exc: json.JSONDecodeError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Configuration must be a valid JSON object"},
    )


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8080, log_level="info", reload = True)
    print("running")