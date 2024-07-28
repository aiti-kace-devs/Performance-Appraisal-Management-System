from typing import List, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.base_class import UUID
from domains.appraisal.respository.appraisal_configuration import appraisal_configuration_actions as appraisal_configuration_repo
from domains.appraisal.schemas.appraisal_configuration import AppraisalConfigurationSchema, AppraisalConfigurationUpdate, AppraisalConfigurationCreate, AppraisalConfigurationWithCycleSchema
from domains.appraisal.schemas.appraisal_cycle import AppraisalCycleSchema
from domains.appraisal.models.appraisal_cycle import AppraisalCycle
from domains.appraisal.models.appraisal_configuration import AppraisalConfiguration
import uuid
#from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import  TEXT
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import TEXT



class AppraisalConfigurationService:


    def list_appraisal_configuration(self, *, db: Session, skip: int = 0, limit: int = 100) -> List[AppraisalConfigurationSchema]:
        appraisal_configuration = appraisal_configuration_repo.get_all(db=db, skip=skip, limit=limit)
        return appraisal_configuration

    def create_appraisal_configuration(self, *, db: Session, appraisal_configuration: AppraisalConfigurationCreate) -> AppraisalConfigurationSchema:
        #print("payload: ", appraisal_configuration)
        if not db.query(AppraisalCycle).filter(AppraisalCycle.id == appraisal_configuration.appraisal_cycles_id).first():
            print("errrrr")
            raise ValueError('appraisal_cycles_id must reference an existing row in the appraisal_cycle table')
        else:
            db.query(AppraisalConfiguration).filter(AppraisalConfiguration.appraisal_cycles_id == str(appraisal_configuration.appraisal_cycles_id).strip()).first()
            #print("var: ", var)
        if db.query(AppraisalConfiguration).filter(AppraisalConfiguration.appraisal_cycles_id == str(appraisal_configuration.appraisal_cycles_id).strip()).first():
            raise ValueError('appraisal_cycles_id already exist in table \'appraisal_configurations\' ' )

        appraisal_configuration_ = appraisal_configuration_repo.create(db=db, obj_in=appraisal_configuration)
        return appraisal_configuration_

    def update_appraisal_configuration(self, *, db: Session, id: UUID, appraisal_configuration: AppraisalConfigurationUpdate) -> AppraisalConfigurationSchema:
        appraisal_configurationobj = appraisal_configuration_repo.get(db=db, id=id)
        if not appraisal_configurationobj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_configuration not found")
        appraisal_configuration_ = appraisal_configuration_repo.update(db=db, db_obj=appraisal_configurationobj, obj_in=appraisal_configuration)
        return appraisal_configuration_

    def get_appraisal_configuration(self, *, db: Session, id: UUID) -> AppraisalConfigurationSchema:
        appraisal_configuration = appraisal_configuration_repo.get(db=db, id=id)
        if not appraisal_configuration:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_configuration not found")
        return appraisal_configuration

    def delete_appraisal_configuration(self, *, db: Session, id: UUID) -> AppraisalConfigurationSchema:
        appraisal_configuration = appraisal_configuration_repo.get(db=db, id=id)
        if not appraisal_configuration:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appraisal_configuration not found")
        appraisal_configuration = appraisal_configuration_repo.remove(db=db, id=id)
        return appraisal_configuration

    def get_appraisal_configuration_by_id(self, *, id: UUID) -> AppraisalConfigurationSchema:
        appraisal_configuration = appraisal_configuration_repo.get(id)
        if not appraisal_configuration:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="appraisal_configuration not found"
            )
        return appraisal_configuration


    def get_appraisal_configuration_by_keywords(self, *, db: Session, tag: str) -> Any:
        if not tag:
            return []

        try:
            # Check if the search term is a valid UUID4
            search_uuid = uuid.UUID(tag.strip(), version=4)

                # Query for the matching appraisal_configuration and its related appraisal_cycle
            result = (
                db.query(AppraisalConfiguration, AppraisalCycle)
                .join(AppraisalCycle, AppraisalConfiguration.appraisal_cycles_id == AppraisalCycle.id)
                .filter(
                    (AppraisalConfiguration.id == search_uuid) |
                    (AppraisalConfiguration.appraisal_cycles_id == search_uuid)
                )
                .first()
            )

            if result:
                appraisal_configuration, appraisal_cycle = result
                return AppraisalConfigurationWithCycleSchema(
                    **appraisal_configuration.__dict__,
                    appraisal_cycle=AppraisalCycleSchema.model_construct(**appraisal_cycle.__dict__) if appraisal_cycle else None
                )

        except ValueError:
            # If not a valid UUID, search by keys in the configuration field
           
            search_key = f'%"{tag}"%'
            results = db.query(AppraisalConfiguration).filter(
                cast(AppraisalConfiguration.configuration, TEXT).ilike(search_key)
            ).all()

            if results:
                return [AppraisalConfigurationSchema.model_construct(**result.__dict__) for result in results]
            
        raise HTTPException(status_code=404, detail="No matching records found")


    



    def search_appraisal_configuration(self, *, db: Session, search: str, value: str) -> List[AppraisalConfigurationSchema]:
        pass

    def read_by_kwargs(self, *, db: Session, **kwargs) -> Any:
        return appraisal_configuration_repo.get_by_kwargs(self, db, kwargs)


appraisal_configuration_service = AppraisalConfigurationService()