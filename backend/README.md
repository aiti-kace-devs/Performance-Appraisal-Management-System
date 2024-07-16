# PROJECT DESCRIPTION

## Ready to set up the project:
    git clone https://github.com/aiti-kace-devs/Performance-Appraisal-Management-System.git


## Installing Packages for Windows
- Run the following command in your terminal
    - cd app
    - pip install -r requirements.txt

## Installing Packages for Linux, Ubuntu
- Run the following command in your terminal
    - cd app
    - python3 -m venv venv
    - source venv/bin/activate
    - pip install -r requirements.txt

## Create Environment File
>  cp .env.example .env

## CREATION AND MIGRATION OF DATABASE
>  Create a database name: **appraisal_db**


## RUNNING OR STARTING APPLICATION
- Running FastAPI Service Locally
    - uvicorn main:app --reload



- Running FastAPI Service On Docker 
    - Start Docker Service
    - docker-compose build
    - docker-compose up




- Database Migration and Data Seeding
Run the following command
    - python migrate.py




Setup environment variables; allowed environment variables `KEYWORDS`=`VALUES`:

| KEYWORDS | VALUES | DEFAULT VALUE | VALUE TYPE | 
| :------------ | :---------------------: | :------------------: | :------------------: |
| DB_TYPE | | postgresql | string 
| DB_NAME | | appraisal_db | string 
| DB_SERVER | | localhost | string
| DB_USER | | postgres | string 
| DB_PASSWORD | | password | string 
| DB_PORT | | 5432 | integer   
| BASE_URL | | http://localhost:8080/ | string  
| ADMIN_EMAIL | | superadmin@admin.com | string 
| ADMIN_PASSWORD | | openforme | string 
| EMAIL_CODE_DURATION_IN_MINUTES | | 15 | integer 
| ACCESS_TOKEN_DURATION_IN_MINUTES | | 60 | integer 
| REFRESH_TOKEN_DURATION_IN_MINUTES | | 600 | integer 
| PASSWORD_RESET_TOKEN_DURATION_IN_MINUTES | | 15 | integer 
| ACCOUNT_VERIFICATION_TOKEN_DURATION_IN_MINUTES | | 15 | integer 
| MAIL_USERNAME | | | string 
| MAIL_PASSWORD | | | string 
| MAIL_FROM | | | string 
| MAIL_PORT | | | string 
| MAIL_SERVER | | | string 
| MAIL_FROM_NAME | | | string 
| MAIL_TLS |  boolean 
| MAIL_SSL | | false | boolean 
| USE_CREDENTIALS |  boolean 
| VALIDATE_CERTS |  boolean 
| DEFAULT_MAIL_SUBJECT | | | string 





For more info on Fastapi: [Click here](https://fastapi.tiangolo.com/)
