from domains.appraisal.models.appraisal import APIBase
from domains.appraisal.models.staff import APIBase
from db.session import engine




def create_tables():
    APIBase.metadata.create_all(bind=engine)