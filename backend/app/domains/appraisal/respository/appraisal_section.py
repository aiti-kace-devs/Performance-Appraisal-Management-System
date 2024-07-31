from crud.base import CRUDBase
from domains.appraisal.models.appraisal_section import AppraisalSection
from domains.appraisal.schemas.appraisal_section import (
    AppraisalSectionCreate, AppraisalSectionUpdate
)


class CRUDAppraisalSection(CRUDBase[AppraisalSection, AppraisalSectionCreate, AppraisalSectionUpdate]):
    pass
appraisal_section_actions = CRUDAppraisalSection(AppraisalSection)