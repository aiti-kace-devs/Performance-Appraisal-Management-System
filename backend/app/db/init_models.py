from domains.appraisal.models.appraisal_configuration import APIBase
from domains.appraisal.models.appraisal_submission import APIBase
from domains.appraisal.models.appraisal_section import APIBase
# from domains.appraisal.models.staff_permissions import APIBase
from domains.appraisal.models.staff_role_permissions import APIBase
from domains.appraisal.models.competency_bank import APIBase
from domains.appraisal.models.appraisal_cycle import APIBase
from domains.appraisal.models.appraisal_form import APIBase
from domains.appraisal.models.staff_deadline import APIBase
from domains.appraisal.models.department import APIBase
from domains.appraisal.models.appraisal import APIBase
from domains.appraisal.models.kra_bank import APIBase
# from domains.appraisal.models.staff import APIBase
from domains.auth.models.users import APIBase
from domains.auth.models.refresh_token import APIBase
from db.session import engine
from sqlalchemy import MetaData


def create_tables():
    APIBase.metadata.create_all(bind=engine)

    #APIBase.metadata.drop_all(bind=engine)

   

