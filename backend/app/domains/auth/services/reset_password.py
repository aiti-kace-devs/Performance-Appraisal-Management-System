from fastapi.response import JSONResponse 
import random 
import string 

class PasswordResetService:

    def generate_reset_token():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=50))