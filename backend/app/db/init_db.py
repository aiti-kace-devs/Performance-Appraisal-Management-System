from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import UUID4
from uuid import uuid4
from sqlalchemy.exc import SQLAlchemyError
# Assuming the correct import for Role and Permission models
# from domains.appraisal.models.roles import Role
# from domains.appraisal.models.permissions import Permission
from domains.appraisal.models.staff_role_permissions import Role, Permission
from domains.auth.models.users import User
from domains.auth.schemas.user_account import UserCreate
from utils.security import pwd_context


SUPER_ADMIN_NAME: str = "Super Admin"
SUPER_ADMIN_PHONE_NUMBER: str = "9876543210"
SUPER_ADMIN_EMAIL: str = "superadmin@admin.com"
SUPER_ADMIN_PASSWORD: str = "openforme"
SUPER_ADMIN_ROLE: str = "super_admin"
SUPER_ADMIN_STATUS: bool = True


def init_db(db: Session):
    """
    Initialize the database with predefined roles and permissions.
    """
    roles_permissions = {
        "super_admin": [
            "createDepartment", "readDepartment", "updateDepartment", "deleteDepartment", 
            "getDepartmentByID", "readAllStaffUnderDepartment", "createStaff", "readStaff",
            "updateStaff", "deleteStaff", "getStaffByID", "uploadStaff", "readAppraisalCycle",
            "getAppraisalCycleByID", "readAppraisalConfiguration", "searchAppraisalConfigurationByKeyword", 
            "getAppraisalConfigurationByID", "readAppraisalSection", "getAppraisalSectionByID", 
            "readCompetencyBank", "getCompetencyBankByID", "readStaffDeadline", "getStaffDeadlineByID", 
            "readKRABank", "getKRABankByID", "readRolePermission", "getRolePermissionByRoleID", 
            "readRoles", "getRoleByID", "updateRole", "addPermissionToRole", "readPermissions", 
            "updatePermission", "getPermissionByID"
        ],
        "hr": [
        "createDepartment","readDepartment","updateDepartment", "deleteDepartment","getDepartmentByID",
        "readAllStaffUnderDepartment","createStaff","readStaff","updateStaff","deleteStaff","getStaffByID",
        "uploadStaff","createAppraisalCycle","readAppraisalCycle", "updateAppraisalCycle",
        "deleteAppraisalCycle","getAppraisalCycleByID","readAppraisalConfiguration","updateAppraisalConfiguration",
        "searchAppraisalConfigurationByKeyword","deleteAppraisalConfiguration","getAppraisalConfigurationByID",
        "readAppraisalSection","getAppraisalSectionByID","readCompetencyBank","getCompetencyBankByID",
        "readAppraisalForm","getAppraisalFormByID","createAppraisalSubmission","readAppraisalSubmission",
        "updateAppraisalSubmission","getAppraisalSubmissionByID","readStaffPermission","updateStaffPermission",
        "deleteStaffPermission","getStaffPermissionByID","readStaffDeadline","getStaffDeadlineByID",
        "readKRABank","getKRABankByID", "readRolePermission","getRolePermissionByRoleID","removeRolePermission",
        "readRoles","getRoleByID","updateRole","addPermissionToRole","readPermissions",
        "updatePermission","getPermissionByID", "approveAppraisal","commentAppraisal"
        ],
        "supervisor": [
           "readDepartment","getDepartmentByID", "readAppraisalCycle","getAppraisalCycleByID", "readAppraisalConfiguration",
           "getAppraisalConfigurationByID","eadAppraisalSection","getAppraisalSectionByID","readCompetencyBank",
           "getCompetencyBankByID","createAppraisalForm","readAppraisalForm","updateAppraisalForm",
           "getAppraisalFormByID","submitAppraisalForm","readAppraisalSubmission","updateAppraisalSubmission",
           "getAppraisalSubmissionByID","createStaffDeadline","getStaffDeadlineByID"
        ],
        "staff": [
        "readDepartment","getDepartmentByID", "readAllStaffUnderDepartment", "readStaff",
        "getStaffByID","readAppraisalCycle","getAppraisalCycleByID","createAppraisalConfiguration","readAppraisalConfiguration",
        "updateAppraisalConfiguration","searchAppraisalConfigurationByKeyword","deleteAppraisalConfiguration","getAppraisalConfigurationByID",
        "createAppraisalSection","readAppraisalSection","upateAppraisalSection","deleteAppraisalSection","getAppraisalSectionByID",
        "createCompetencyBank","readCompetencyBank","updateCompetencyBank","deletCompetencyBank","getCompetencyBankByID",
        "createAppraisalForm","readAppraisalForm","updateAppraisalForm","getAppraisalFormByID",
        "createAppraisalSubmission","readAppraisalSubmission","updateAppraisalSubmission",
        "getAppraisalSubmissionByID","createStaffDeadline","readStaffDeadline","updateStaffDeadline",
        "getStaffDeadlineByID","createKRABank","readKRABank","updateKRABank",
        "deleteKRABank","getKRABankByID","approveAppraisal","commentAppraisal"
        ]
    }

    try:
        # Create roles and permissions
        for role_name, permission_names in roles_permissions.items():
            # Check if the role already exists
            role = db.query(Role).filter(Role.name == role_name).first()
            if not role:
                # Create the role if it doesn't exist
                role = Role(id=uuid4(), name=role_name)
                db.add(role)

            # Check and assign permissions
            for perm_name in permission_names:
                try:
                    permission = db.query(Permission).filter(Permission.name == perm_name).first()
                    if not permission:
                        # Create permission if it doesn't exist
                        permission = Permission(id=uuid4(), name=perm_name)
                        db.add(permission)
                        db.flush()  # Flushes the changes to the DB before committing
                        # return f"Created permission: {perm_name}"  # Debug log
                    else:
                        # return f"Permission {perm_name} already exists"  # Debug log
                        pass

                    # Assign permission to the role if not already assigned
                    if permission not in role.permissions:
                        role.permissions.append(permission)
                except IntegrityError:
                    db.rollback()  # Roll back the transaction in case of duplicate
                    # return f"IntegrityError: Permission {perm_name} already exists. Skipping."
            
        # Commit the role-permission association to the database once
        db.commit()
        return "Roles and permissions initialized successfully."
    
    except SQLAlchemyError as e:
        db.rollback()
        return f"Error initializing roles and permissions: {str(e)}"

def create_super_admin(db: Session):
    """
    Create the initial super admin user if they don't exist.
    
    """
    
    try:
        # Check if super admin user exists
        admin = db.query(User).filter(User.email == SUPER_ADMIN_EMAIL).first()
        
        # Check if super admin role exists
        role = db.query(Role).filter(Role.name == 'super_admin').first()
        
        if not role:
            raise HTTPException(status_code=400, detail="Super Admin role not found")
        
        # If the super admin doesn't exist, create it
        if not admin:
            admin_in = User(
                email=SUPER_ADMIN_EMAIL,
                password=pwd_context.hash(SUPER_ADMIN_PASSWORD),
                reset_password_token=None,
                staff_id=uuid4(),
                role_id=role.id
            )
            db.add(admin_in)
            db.commit()
            db.refresh(admin_in)
            print("Super admin user created successfully.")
    
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating super admin: {str(e)}")
