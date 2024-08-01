from typing import Any
from sqlalchemy import JSON, Boolean, Column, Date, DateTime, ForeignKey, String, Text,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase





class AppraisalCycle(APIBase):


    name = Column(String, unique=True, nullable=False) 
    description = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    appraisal = relationship('Appraisal', backref='appraisals', uselist=False, cascade='all, delete-orphan')
    appraisal_configuration = relationship('AppraisalConfiguration', backref='appraisal_configurations', uselist=False, cascade='all, delete-orphan')
    appraisal_section = relationship('AppraisalSection', backref='appraisal_sections', uselist=False, cascade='all, delete-orphan')
    

    



