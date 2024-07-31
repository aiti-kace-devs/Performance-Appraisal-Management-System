from crud.base import CRUDBase
from domains.appraisal.models.users import User
from domains.appraisal.schemas.users import (
    UserCreate, UserUpdate
)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass
users_form_actions = CRUDUser(User)
