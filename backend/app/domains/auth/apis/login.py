from fastapi import FastAPI, APIRouter,Depends,status,Response,Cookie,Request
from domains.auth.services.user_account import users_forms_service
from domains.auth.models.refresh_token import RefreshToken
from domains.auth.models.users import User
from fastapi.security import OAuth2PasswordRequestForm
from domains.auth.schemas import auth as schema
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from config.settings import settings
from utils.security import Security
from sqlalchemy.orm import Session
from datetime import timedelta
from db.session import get_db
from fastapi_limiter.depends import RateLimiter
from domains.auth.services.login import login_service
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware


app = FastAPI()

# Authentication module for admins and users
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

# Initialize the Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
#app.add_exception_handler(RateLimitExceeded, limiter._rate_limit_exceeded_handler)

# Add SlowAPI middleware
app.add_middleware(SlowAPIMiddleware)

# Custom exception handler for rate limiting
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return Response(
        content="Rate limit exceeded, resulting in the account been locked.\nPlease try again in 10minutes later.",
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    )



@auth_router.post("/token")
@limiter.limit("3/minute")  # Brute force protection
async def login_for_access_token(request: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        # Attempt to log in the user
        user_sign_in = login_service.log_user_in(response=response, db=db, form_data=form_data)
        return user_sign_in

    except HTTPException as ex:
        if ex.status_code == status.HTTP_401_UNAUTHORIZED:
            print("ex error: ", ex)
            return Response(content=str(ex.detail), status_code=ex.status_code)
        else:
            # Handle specific HTTP exceptions
            return Response(content=str(ex.detail), status_code=ex.status_code)

    except RateLimitExceeded as ex:
        # Handle rate limit exceeded
        user = db.query(User).filter(User.email == form_data.username).first()
        if user:
            user.lock_account(lock_time_minutes=10)
            db.commit()
        return Response(
            content="Account locked due to too many attempts, please try again in 10 minutes.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    except Exception as ex:
        # Handle all other exceptions
        print("Unexpected error in login: ", ex)
        return Response(content="An unexpected error occurred. Please try again later.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)




@auth_router.get("/logged_in_users")
async def get_logged_in_users(request: Request, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    online_users= login_service.list_logged_in_users(request, db, skip=skip, limit=limit)
    print("active online users: ", online_users)
    return online_users



@auth_router.post("/refresh")
def get_new_access_token(response:Response, refresh_token: schema.Token, db: Session = Depends(get_db)):

    refresh_token_check = db.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token.refresh_token).first()
    if not refresh_token_check:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Could not validate new access token credentials",
                        headers={"WWW-Authenticate": "Bearer"}
                        )
    
    user_data = users_forms_service.get_user_by_id(db=db, id=refresh_token_check.user_id)


    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_DURATION_IN_MINUTES)
    new_access_token = Security.create_access_token(data={"email": user_data.email}, expires_delta=access_token_expires)
    new_refresh_token = Security.create_refresh_token(jsonable_encoder(user_data))


    # delete user refresh token after requesting for a new access token
    refresh_token_check = db.query(RefreshToken).filter(RefreshToken.user_id == user_data.id)
    if refresh_token_check.first():
        refresh_token_check.delete()
        db.commit()


    refresh_token_dict = {
        "user_id": user_data.id,
        "refresh_token": new_refresh_token,
    }

    # create new refresh token for user after requesting for a new access token
    refresh_token_data= RefreshToken(**refresh_token_dict)
    db.add(refresh_token_data)
    db.commit()
    

    return {
        "access_token": new_access_token,
        "token_type":"bearer",
        "refresh_token":new_refresh_token,
        "status": status.HTTP_200_OK
        }


