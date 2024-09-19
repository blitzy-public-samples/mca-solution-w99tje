import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.api.controllers.webhook_controller import create_webhook, get_webhook, get_webhooks, update_webhook, delete_webhook, test_webhook
from src.api.models.webhook import Webhook, WebhookEventType
from src.api.schemas.webhook_schema import WebhookCreate, WebhookUpdate
from src.api.models.user import User
from src.services.webhook_service import WebhookService

@pytest.mark.asyncio
async def test_create_webhook(db_session: Session, mock_user: User):
    # Create a mock WebhookCreate object
    webhook_create = WebhookCreate(
        url="https://example.com/webhook",
        event_type=WebhookEventType.APPLICATION_SUBMITTED,
        is_active=True
    )

    # Mock the WebhookService.validate_webhook_url method to return True
    WebhookService.validate_webhook_url = lambda _: True

    # Call create_webhook with the mock object
    created_webhook = await create_webhook(db_session, webhook_create, mock_user)

    # Assert that the returned webhook has the correct attributes
    assert created_webhook.url == webhook_create.url
    assert created_webhook.event_type == webhook_create.event_type
    assert created_webhook.is_active == webhook_create.is_active
    assert created_webhook.user_id == mock_user.id

    # Verify that the webhook was added to the database session
    assert created_webhook in db_session.new

    # Test creating a webhook with an invalid URL and assert it raises an HTTPException
    WebhookService.validate_webhook_url = lambda _: False
    with pytest.raises(HTTPException):
        await create_webhook(db_session, webhook_create, mock_user)

@pytest.mark.asyncio
async def test_get_webhook(db_session: Session, mock_user: User):
    # Create a mock Webhook object and add it to the database session
    mock_webhook = Webhook(id=1, url="https://example.com/webhook", event_type=WebhookEventType.APPLICATION_SUBMITTED, is_active=True, user_id=mock_user.id)
    db_session.add(mock_webhook)
    db_session.commit()

    # Call get_webhook with the mock webhook's ID
    retrieved_webhook = await get_webhook(db_session, mock_webhook.id, mock_user)

    # Assert that the returned webhook matches the mock webhook
    assert retrieved_webhook.id == mock_webhook.id
    assert retrieved_webhook.url == mock_webhook.url
    assert retrieved_webhook.event_type == mock_webhook.event_type
    assert retrieved_webhook.is_active == mock_webhook.is_active

    # Test with a non-existent ID and assert that it raises an HTTPException
    with pytest.raises(HTTPException):
        await get_webhook(db_session, 999, mock_user)

@pytest.mark.asyncio
async def test_get_webhooks(db_session: Session, mock_user: User):
    # Create multiple mock Webhook objects and add them to the database session
    webhooks = [
        Webhook(id=i, url=f"https://example.com/webhook{i}", event_type=WebhookEventType.APPLICATION_SUBMITTED, is_active=True, user_id=mock_user.id)
        for i in range(1, 6)
    ]
    db_session.add_all(webhooks)
    db_session.commit()

    # Call get_webhooks with various skip and limit parameters
    all_webhooks = await get_webhooks(db_session, mock_user, skip=0, limit=100)
    assert len(all_webhooks) == 5

    first_two = await get_webhooks(db_session, mock_user, skip=0, limit=2)
    assert len(first_two) == 2
    assert first_two[0].id == 1
    assert first_two[1].id == 2

    last_three = await get_webhooks(db_session, mock_user, skip=2, limit=3)
    assert len(last_three) == 3
    assert last_three[0].id == 3
    assert last_three[2].id == 5

    # Test pagination by verifying that different subsets of webhooks are returned with different skip/limit values
    middle_two = await get_webhooks(db_session, mock_user, skip=1, limit=2)
    assert len(middle_two) == 2
    assert middle_two[0].id == 2
    assert middle_two[1].id == 3

@pytest.mark.asyncio
async def test_update_webhook(db_session: Session, mock_user: User):
    # Create a mock Webhook object and add it to the database session
    mock_webhook = Webhook(id=1, url="https://example.com/webhook", event_type=WebhookEventType.APPLICATION_SUBMITTED, is_active=True, user_id=mock_user.id)
    db_session.add(mock_webhook)
    db_session.commit()

    # Create a mock WebhookUpdate object with updated values
    webhook_update = WebhookUpdate(
        url="https://example.com/updated",
        event_type=WebhookEventType.APPLICATION_APPROVED,
        is_active=False
    )

    # Mock the WebhookService.validate_webhook_url method to return True
    WebhookService.validate_webhook_url = lambda _: True

    # Call update_webhook with the mock webhook's ID and update object
    updated_webhook = await update_webhook(db_session, mock_webhook.id, webhook_update, mock_user)

    # Assert that the returned webhook has the updated attributes
    assert updated_webhook.url == webhook_update.url
    assert updated_webhook.event_type == webhook_update.event_type
    assert updated_webhook.is_active == webhook_update.is_active

    # Verify that the webhook in the database session was updated
    db_session.refresh(mock_webhook)
    assert mock_webhook.url == webhook_update.url
    assert mock_webhook.event_type == webhook_update.event_type
    assert mock_webhook.is_active == webhook_update.is_active

    # Test with a non-existent ID and assert that it raises an HTTPException
    with pytest.raises(HTTPException):
        await update_webhook(db_session, 999, webhook_update, mock_user)

    # Test updating a webhook with an invalid URL and assert it raises an HTTPException
    WebhookService.validate_webhook_url = lambda _: False
    with pytest.raises(HTTPException):
        await update_webhook(db_session, mock_webhook.id, webhook_update, mock_user)

@pytest.mark.asyncio
async def test_delete_webhook(db_session: Session, mock_user: User):
    # Create a mock Webhook object and add it to the database session
    mock_webhook = Webhook(id=1, url="https://example.com/webhook", event_type=WebhookEventType.APPLICATION_SUBMITTED, is_active=True, user_id=mock_user.id)
    db_session.add(mock_webhook)
    db_session.commit()

    # Call delete_webhook with the mock webhook's ID
    await delete_webhook(db_session, mock_webhook.id, mock_user)

    # Assert that the webhook was removed from the database session
    assert db_session.query(Webhook).filter(Webhook.id == mock_webhook.id).first() is None

    # Test with a non-existent ID and assert that it raises an HTTPException
    with pytest.raises(HTTPException):
        await delete_webhook(db_session, 999, mock_user)

@pytest.mark.asyncio
async def test_test_webhook(db_session: Session, mock_user: User):
    # Create a mock Webhook object and add it to the database session
    mock_webhook = Webhook(id=1, url="https://example.com/webhook", event_type=WebhookEventType.APPLICATION_SUBMITTED, is_active=True, user_id=mock_user.id)
    db_session.add(mock_webhook)
    db_session.commit()

    # Mock the WebhookService.trigger_webhook method to return a success status
    WebhookService.trigger_webhook = lambda *args, **kwargs: True

    # Call test_webhook with the mock webhook's ID
    test_result = await test_webhook(db_session, mock_webhook.id, mock_user)

    # Assert that the returned result indicates a successful test
    assert test_result["success"] is True
    assert "Webhook test successful" in test_result["message"]

    # Mock the WebhookService.trigger_webhook method to return a failure status
    WebhookService.trigger_webhook = lambda *args, **kwargs: False

    # Call test_webhook with the mock webhook's ID
    test_result = await test_webhook(db_session, mock_webhook.id, mock_user)

    # Assert that the returned result indicates a failed test
    assert test_result["success"] is False
    assert "Webhook test failed" in test_result["message"]

    # Test with a non-existent ID and assert that it raises an HTTPException
    with pytest.raises(HTTPException):
        await test_webhook(db_session, 999, mock_user)