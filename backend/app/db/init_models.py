from domains.appraisal.models.appraisal_configuration import APIBase
from domains.appraisal.models.appraisal_cycle import APIBase
from domains.appraisal.models.appraisal_form import APIBase
from domains.appraisal.models.appraisal_section import APIBase
from domains.appraisal.models.appraisal_submission import APIBase
from domains.appraisal.models.appraisal import APIBase
from domains.appraisal.models.competency_bank import APIBase
from domains.appraisal.models.department import APIBase
from domains.appraisal.models.staff_deadline import APIBase
from domains.appraisal.models.staff_permissions import APIBase
from domains.appraisal.models.staff import APIBase
from domains.appraisal.models.users import APIBase
from domains.appraisal.models.kra_bank import APIBase
# from domains.appraisal.models.role_permissions import APIBase
from domains.appraisal.models.roles import APIBase
# from domains.appraisal.models.permissions import APIBase
from domains.appraisal.models.users import APIBase
from db.session import engine



def create_tables():
    APIBase.metadata.create_all(bind=engine)
   

