from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from src.api.models.webhook import Webhook
from src.api.schemas.webhook_schema import WebhookCreate, WebhookUpdate, WebhookResponse
from src.core.database import get_db
from src.core.security import get_current_user
from src.services.webhook_service import WebhookService
from src.utils.logger import logger

router = APIRouter()

@router.post('/', response_model=WebhookResponse)
def create_webhook(webhook: WebhookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Validate webhook URL using WebhookService
    WebhookService.validate_url(webhook.url)

    # Create new Webhook instance
    new_webhook = Webhook(**webhook.dict(), user_id=current_user.id)

    # Add webhook to database session
    db.add(new_webhook)

    # Commit changes to database
    db.commit()
    db.refresh(new_webhook)

    # Log webhook creation
    logger.info(f"Webhook created: {new_webhook.id}")

    # Return created webhook
    return new_webhook

@router.get('/{webhook_id}', response_model=WebhookResponse)
def get_webhook(webhook_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Query database for webhook with given ID
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id, Webhook.user_id == current_user.id).first()

    # If webhook not found, raise HTTPException
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    # Return found webhook
    return webhook

@router.get('/', response_model=List[WebhookResponse])
def get_webhooks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Query database for webhooks with pagination
    webhooks = db.query(Webhook).filter(Webhook.user_id == current_user.id).offset(skip).limit(limit).all()

    # Return list of webhooks
    return webhooks

@router.patch('/{webhook_id}', response_model=WebhookResponse)
def update_webhook(webhook_id: int, webhook_update: WebhookUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Query database for webhook with given ID
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id, Webhook.user_id == current_user.id).first()

    # If webhook not found, raise HTTPException
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    # If URL is being updated, validate new URL using WebhookService
    if webhook_update.url:
        WebhookService.validate_url(webhook_update.url)

    # Update webhook with new data
    for key, value in webhook_update.dict(exclude_unset=True).items():
        setattr(webhook, key, value)

    # Commit changes to database
    db.commit()
    db.refresh(webhook)

    # Log webhook update
    logger.info(f"Webhook updated: {webhook.id}")

    # Return updated webhook
    return webhook

@router.delete('/{webhook_id}')
def delete_webhook(webhook_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Query database for webhook with given ID
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id, Webhook.user_id == current_user.id).first()

    # If webhook not found, raise HTTPException
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    # Delete webhook from database
    db.delete(webhook)

    # Commit changes to database
    db.commit()

    # Log webhook deletion
    logger.info(f"Webhook deleted: {webhook_id}")

    # Return confirmation message
    return {"message": "Webhook deleted successfully"}

@router.post('/{webhook_id}/test')
def test_webhook(webhook_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Query database for webhook with given ID
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id, Webhook.user_id == current_user.id).first()

    # If webhook not found, raise HTTPException
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    # Generate sample payload using WebhookService
    sample_payload = WebhookService.generate_sample_payload()

    # Send test payload to webhook URL using WebhookService
    test_result = WebhookService.send_test_payload(webhook.url, sample_payload)

    # Log test result
    logger.info(f"Webhook test result for {webhook_id}: {test_result}")

    # Return test result
    return {"result": test_result}