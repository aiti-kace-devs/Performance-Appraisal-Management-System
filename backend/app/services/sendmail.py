from fastapi_mail import ConnectionConfig,FastMail,MessageSchema
from models.models import Event,Participants,User,UploadedFile
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from config.settings import Settings
from typing import List,Any,Dict
from jinja2 import Environment, select_autoescape, PackageLoader
import os
from fastapi import Response, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import UUID4
from services import date_time_format
from datetime import datetime 

env = Environment(
    loader=PackageLoader('templates', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)



class EmailSchema(BaseModel):
    email: List[EmailStr]
    # body: Dict[str, Any]



class Email:
    def __init__(self,  user: User,  url: str,  email: EmailSchema,  db: Session):

        self.name = user.name
        self.sender = Settings.MAIL_USERNAME
        self.email = email
        self.url = url
        pass


    async def sendMailService(self, subject, template, message_body: str) -> JSONResponse:
        
        
      

        conf = ConnectionConfig(
            MAIL_USERNAME = Settings.MAIL_USERNAME,
            MAIL_PASSWORD = Settings.MAIL_PASSWORD,
            MAIL_FROM =  Settings.MAIL_FROM,
            MAIL_PORT = Settings.MAIL_PORT,
            MAIL_SERVER = Settings.MAIL_SERVER,
            MAIL_STARTTLS = Settings.MAIL_STARTTLS,
            MAIL_SSL_TLS = Settings.MAIL_SSL_TLS,
            USE_CREDENTIALS = Settings.USE_CREDENTIALS,
            VALIDATE_CERTS = Settings.VALIDATE_CERTS
        )

 
        # Generate the HTML template base on the template name
        template = env.get_template(f'{template}.html')

        html = template.render(
            url=self.url,
            name=self.name,
            email=self.email,
            subject=subject,
            body=self.message_body
        )


        # self.qr_code_image.seek(0)
        # Define the message options
        message = MessageSchema(
            subject=subject,
            recipients=self.email,
            body=html,
            subtype="html",

        )


        # Send the email
        fm = FastMail(conf)
        await fm.send_message(message)

       
        


    async def email_to_reset_password(self):
        await self.sendMailService(self.message_body, 'send_email_to_registered_participant',)

 