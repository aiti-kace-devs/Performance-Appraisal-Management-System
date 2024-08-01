from crud.base import CRUDBase
from domains.appraisal.models.appraisal_configuration import AppraisalConfiguration
from domains.appraisal.schemas.appraisal_configuration import (
    AppraisalConfigurationCreate, AppraisalConfigurationUpdate
)


class CRUDAppraisalConfiguration(CRUDBase[AppraisalConfiguration, AppraisalConfigurationCreate, AppraisalConfigurationUpdate]):
    pass

appraisal_configuration_actions = CRUDAppraisalConfiguration(AppraisalConfiguration)