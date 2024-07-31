from domains.appraisal.models.appraisal import APIBase
from domains.appraisal.models.appraisal_submission import APIBase
from domains.appraisal.models.appraisal_configuration import APIBase
from domains.appraisal.models.appraisal_cycle import APIBase
from domains.appraisal.models.appraisal_section import APIBase
from db.session import engine



def create_tables():
    APIBase.metadata.create_all(bind=engine)