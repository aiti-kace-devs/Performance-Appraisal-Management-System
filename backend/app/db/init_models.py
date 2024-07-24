from domains.appraisal.models.appraisal import APIBase
from domains.appraisal.models.roles import APIBase
from domains.appraisal.models.permissions import APIBase
from db.session import engine




def create_tables():
    APIBase.metadata.create_all(bind=engine)