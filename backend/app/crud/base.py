import sys
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic import UUID4
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):  # 1

    def __init__(self, model: Type[ModelType]):  # 2
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    async def read(self, db: Session, search: str = None, value: str = None, skip: int = 0, limit: int = 100):
        base = db.query(self.model)
        if search and value:
            try:
                base = base.filter(
                    self.model.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                return base.offset(skip).limit(limit).all()
        return base.offset(skip).limit(limit).all()

    def iread(self, db: Session, value: str = None):
        search = "name"
        base = db.query(self.model)
        response = []
        # print("search: ", search)
        # print("value: ", value)
        # print("saerch and value: ", (search and value))
        if search and value:
            try:
                response = base.filter(
                    self.model.__table__.c[search].ilike("%" + value + "%"))
                # print("response:: ", response.all())
                if not response.all():
                    response = base.filter(
                    self.model.__table__.c["year"] == value)
                # print("base: ", response)
            except KeyError as ke:
                # print("ke.json: ", ke.json())
                return ke.json()
        return response.all()

    async def read_by_id(self, id, db: Session):
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all_by_ids(self, db: Session, ids: List[Any]) -> Optional[List[ModelType]]:
        if ids is None:
            ids = []
        return db.query(self.model).filter(self.model.id.in_(ids)).all()

    def get_by_id(self, id: Any, db: Session) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:

        try:
            if not obj_in:
                return None
            # from datetime import datetime
            # obj_in.created_at = datetime.utcnow()
            # obj_in.updated_at = obj_in.created_at

            obj_in_data = obj_in.dict()
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=409, detail="{}".format(sys.exc_info()[1]))

        except Exception as ex:
            db.rollback()
            import traceback
            print(''.join(traceback.TracebackException.from_exception(ex).format()))

            raise HTTPException(status_code=500, detail="{}: {}".format(
                sys.exc_info()[0], sys.exc_info()[1]))

    def _update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:

        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
                db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        try:
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as ex:
            db.rollback()
            import traceback
            print(''.join(traceback.TracebackException.from_exception(ex).format()))
            raise HTTPException(status_code=500, detail="{}: {}".format(
                sys.exc_info()[0], sys.exc_info()[1])
                                )

    def remove(self, db: Session, *, id: UUID4) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    async def filter_range(self, db: Session, skip: int = 0, limit: int = 100, search: str = None,
                           lower_boundary: float = 0, upper_boundary: float = 0):
        try:
            base = db.query(self.model)
            if lower_boundary and upper_boundary:
                try:
                    base = base.filter(and_(
                        self.model.__table__.c[search] <= upper_boundary,
                        self.model.__table__.c[search] >= lower_boundary
                    ))
                except KeyError:
                    return base.offset(skip).limit(limit).all()
            return base.offset(skip).limit(limit).all()
        except:
            raise HTTPException(
                status_code=500, detail="{}".format(sys.exc_info()[1]))
