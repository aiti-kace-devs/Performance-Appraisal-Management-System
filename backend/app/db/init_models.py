from domains.appraisal.models.appraisal import APIBase
from domains.appraisal.models.appraisal_form import APIBase
from db.session import engine




def create_tables():
    APIBase.metadata.create_all(bind=engine)