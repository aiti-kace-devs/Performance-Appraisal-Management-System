from fastapi import FastAPI, APIRouter,Depends,Response,Request
from sqlalchemy.orm import Session
from db.session import get_db
from domains.auth.services.logout import logoutservice



app = FastAPI()

# Authentication module for admins and users
logout_auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)





@logout_auth_router.post("/logout")
async def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    return await logoutservice.logout_user(request, response, db)