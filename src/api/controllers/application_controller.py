from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from src.api.models.application import Application
from src.api.schemas.application_schema import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from src.core.database import get_db
from src.core.security import get_current_user
from src.services.data_validator import DataValidator
from src.services.webhook_service import WebhookService

router = APIRouter()

@router.post('/', response_model=ApplicationResponse)
async def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ApplicationResponse:
    # Validate application data using DataValidator
    DataValidator.validate_application(application)

    # Create new Application instance
    new_application = Application(**application.dict())

    # Add application to database session
    db.add(new_application)

    # Commit changes to database
    db.commit()
    db.refresh(new_application)

    # Trigger webhook notification for new application
    WebhookService.notify_new_application(new_application)

    # Return created application
    return ApplicationResponse.from_orm(new_application)

@router.get('/{application_id}', response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ApplicationResponse:
    # Query database for application with given ID
    application = db.query(Application).filter(Application.id == application_id).first()

    # If application not found, raise HTTPException
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # Return found application
    return ApplicationResponse.from_orm(application)

@router.get('/', response_model=List[ApplicationResponse])
async def get_applications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[ApplicationResponse]:
    # Query database for applications with pagination
    applications = db.query(Application).offset(skip).limit(limit).all()

    # Return list of applications
    return [ApplicationResponse.from_orm(app) for app in applications]

@router.patch('/{application_id}', response_model=ApplicationResponse)
async def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ApplicationResponse:
    # Query database for application with given ID
    application = db.query(Application).filter(Application.id == application_id).first()

    # If application not found, raise HTTPException
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # Validate updated application data using DataValidator
    DataValidator.validate_application_update(application_update)

    # Update application with new data
    for key, value in application_update.dict(exclude_unset=True).items():
        setattr(application, key, value)

    # Commit changes to database
    db.commit()
    db.refresh(application)

    # Trigger webhook notification for updated application
    WebhookService.notify_updated_application(application)

    # Return updated application
    return ApplicationResponse.from_orm(application)