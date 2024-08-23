from fastapi_mail import ConnectionConfig,FastMail,MessageSchema
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from config.settings import Settings
from typing import List,Any,Dict
from jinja2 import Environment, select_autoescape, PackageLoader
# from jinja2 import Environment, select_autoescape, PackageLoader
import os
from fastapi import Response, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import UUID4
from domains.auth.models.users import User

env = Environment(
    loader=PackageLoader('templates', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)



class EmailSchema(BaseModel):
    email: List[EmailStr]




class Email:
    def __init__(self, url: str, email: EmailSchema):

        # self.name = user.name
        self.sender = Settings.MAIL_USERNAME
        self.email = email
        self.url = url
        # self.db = db
        

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

    async def sendMailService(self, subject, template, message_body: str) -> JSONResponse:
        
        # # Generate the HTML template base on the template name
        template = env.get_template(f'{template}.html')

        html = template.render(
            email=self.email,
            subject=subject,
            url=self.url,
            body=self.message_body
        )


        # Define the message options
        message = MessageSchema(
            subject=subject,
            recipients=[self.email],
            body=html,
            subtype="html",

        )

        # Send the email using FastMail
        fm = FastMail(self.conf)
        await fm.send_message(message)

      