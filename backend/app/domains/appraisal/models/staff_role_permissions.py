
from typing import Any
from sqlalchemy import Column, ForeignKey, String, Table, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.base_class import APIBase


# Define the association table for staff and permissions
staff_permissions = Table(
    'staff_permissions',
    APIBase.metadata,
    # Composite primary key of staff_id and permission_id
    Column('staff_id', UUID(as_uuid=True), ForeignKey("staffs.id"), nullable=False, primary_key=True),
    Column('permission_id',UUID(as_uuid=True), ForeignKey("permissions.id"), nullable=False, primary_key=True)
)

# Define the association table for roles and permissions
role_permissions = Table(
    'role_permissions',
    APIBase.metadata,
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', UUID(as_uuid=True), ForeignKey('permissions.id'), primary_key=True)
)


class Role(APIBase):
    __tablename__ = 'roles'

    name = Column(String(255), unique=True, index=True)
    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )
    staff_members = relationship("Staff", back_populates="role")


class Permission(APIBase):
    __tablename__ = 'permissions'

    name = Column(String(255), unique=True, index=True)

    # Relationship with Role (many-to-many with Role through role_permissions)
    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions"
    )

    # Relationship with Staff (many-to-many with Staff through StaffPermission)
    staffs = relationship(
        "Staff",
        secondary=staff_permissions,  # Junction table
        back_populates="permissions"  # Backpopulates from Staff model
    )


class Staff(APIBase):
    __tablename__ = 'staffs'

    title = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    other_name = Column(String, nullable=True)
    gender = Column(String)
    position = Column(String, nullable=False)
    email = Column(String, unique=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)
    grade = Column(String(255), nullable=False)
    appointment_date = Column(Date, nullable=True)
    
    # Foreign key for Role (Many Staffs can have one Role)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="staff_members")
    department = relationship("Department", back_populates="staff_departments")
    staff_supervisors = relationship("StaffSupervisor", back_populates="staffs")
    appraisal_sections = relationship("AppraisalSection", back_populates="staffs")
    appraisal_cycles = relationship("AppraisalCycle", back_populates="staffs")
    appraisal_forms = relationship("AppraisalForm", back_populates="staffs")

    # Many-to-many relationship with Permission through StaffPermission
    permissions = relationship(
        "Permission", 
        secondary=staff_permissions,  # Junction table
        back_populates="staffs"  # Backpopulates from Permission model
    )
