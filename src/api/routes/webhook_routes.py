from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.api.controllers.webhook_controller import create_webhook, get_webhook, get_webhooks, update_webhook, delete_webhook, test_webhook
from src.api.schemas.webhook_schema import WebhookCreate, WebhookUpdate, WebhookResponse
from src.core.database import get_db
from src.core.security import get_current_user
from src.api.models.user import User

router = APIRouter()

@router.post('/', response_model=WebhookResponse)
def create_new_webhook(webhook: WebhookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Route to create a new webhook
    """
    try:
        # Call create_webhook function from webhook_controller
        new_webhook = create_webhook(db, webhook, current_user)
        # Return the created webhook
        return new_webhook
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('/{webhook_id}', response_model=WebhookResponse)
def read_webhook(webhook_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Route to retrieve a specific webhook by ID
    """
    try:
        # Call get_webhook function from webhook_controller
        webhook = get_webhook(db, webhook_id, current_user)
        # Return the retrieved webhook
        return webhook
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get('/', response_model=List[WebhookResponse])
def read_webhooks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Route to retrieve a list of webhooks with optional filtering and pagination
    """
    # Call get_webhooks function from webhook_controller
    webhooks = get_webhooks(db, current_user, skip=skip, limit=limit)
    # Return the list of webhooks
    return webhooks

@router.patch('/{webhook_id}', response_model=WebhookResponse)
def update_existing_webhook(webhook_id: int, webhook_update: WebhookUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Route to update an existing webhook
    """
    try:
        # Call update_webhook function from webhook_controller
        updated_webhook = update_webhook(db, webhook_id, webhook_update, current_user)
        # Return the updated webhook
        return updated_webhook
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete('/{webhook_id}')
def delete_existing_webhook(webhook_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Route to delete an existing webhook
    """
    try:
        # Call delete_webhook function from webhook_controller
        delete_webhook(db, webhook_id, current_user)
        # Return confirmation message
        return {"message": "Webhook deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post('/{webhook_id}/test')
def test_existing_webhook(webhook_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Route to test an existing webhook by sending a sample payload
    """
    try:
        # Call test_webhook function from webhook_controller
        test_result = test_webhook(db, webhook_id, current_user)
        # Return test result
        return test_result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))