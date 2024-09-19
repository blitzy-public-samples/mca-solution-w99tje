from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.api.controllers.application_controller import create_application, get_application, get_applications, update_application
from src.api.schemas.application_schema import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from src.core.database import get_db
from src.core.security import get_current_user
from src.api.models.user import User

router = APIRouter()

@router.post('/', response_model=ApplicationResponse)
def create_new_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Call create_application function from application_controller
    new_application = create_application(db, application, current_user)
    
    # Return the created application
    return new_application

@router.get('/{application_id}', response_model=ApplicationResponse)
def read_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Call get_application function from application_controller
    application = get_application(db, application_id, current_user)
    
    # Return the retrieved application
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application

@router.get('/', response_model=List[ApplicationResponse])
def read_applications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Call get_applications function from application_controller
    applications = get_applications(db, skip, limit, current_user)
    
    # Return the list of applications
    return applications

@router.patch('/{application_id}', response_model=ApplicationResponse)
def update_existing_application(
    application_id: int,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Call update_application function from application_controller
    updated_application = update_application(db, application_id, application_update, current_user)
    
    # Return the updated application
    if updated_application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return updated_application