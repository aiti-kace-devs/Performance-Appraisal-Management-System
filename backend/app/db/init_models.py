from domains.appraisal.models.appraisal import APIBase #as AppraisalBase
from domains.appraisal.models.appraisal_configuration import APIBase #as Appraisal_ConfigurationBase
from domains.appraisal.models.appraisal_cycle import APIBase #as AppraisalCycleBase
from domains.appraisal.models.appraisal_section import APIBase #as AppraisalSectionBase
from domains.appraisal.models.department import APIBase #as DepartmentBase
from domains.appraisal.models.staff import APIBase #as StaffBase
from domains.appraisal.models.kra_bank import APIBase #as Kra_BankBase
from db.session import engine



def create_tables():
    # APIBase.metadata.drop_all(engine)
    APIBase.metadata.create_all(bind=engine)
   