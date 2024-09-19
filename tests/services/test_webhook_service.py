import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from src.services.webhook_service import WebhookService
from src.api.models.webhook import Webhook, WebhookEventType
from src.core.config import settings

def test_webhook_service_initialization():
    # Create an instance of WebhookService
    webhook_service = WebhookService()
    
    # Assert that the instance is not None
    assert webhook_service is not None
    
    # Assert that the instance is of type WebhookService
    assert isinstance(webhook_service, WebhookService)

@pytest.mark.asyncio
async def test_trigger_webhook():
    # Create a mock database session
    mock_session = Mock(spec=Session)
    
    # Create sample webhooks for different event types
    webhook1 = Webhook(url="http://example.com/webhook1", event_type=WebhookEventType.APPLICATION_SUBMITTED)
    webhook2 = Webhook(url="http://example.com/webhook2", event_type=WebhookEventType.APPLICATION_APPROVED)
    mock_session.query.return_value.filter.return_value.all.return_value = [webhook1, webhook2]
    
    # Mock the requests.post method
    with patch('src.services.webhook_service.requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Create an instance of WebhookService
        webhook_service = WebhookService()
        
        # Call trigger_webhook with different event types and payloads
        await webhook_service.trigger_webhook(mock_session, WebhookEventType.APPLICATION_SUBMITTED, {"application_id": 123})
        await webhook_service.trigger_webhook(mock_session, WebhookEventType.APPLICATION_APPROVED, {"application_id": 456})
        
        # Assert that requests.post was called with correct URLs and payloads
        assert mock_post.call_count == 2
        mock_post.assert_any_call(webhook1.url, json=pytest.approx({"event_type": "APPLICATION_SUBMITTED", "application_id": 123, "timestamp": pytest.approx(int, abs=1)}))
        mock_post.assert_any_call(webhook2.url, json=pytest.approx({"event_type": "APPLICATION_APPROVED", "application_id": 456, "timestamp": pytest.approx(int, abs=1)}))
        
        # Verify that webhook status (last triggered, retry count) was updated correctly
        assert webhook1.last_triggered_at is not None
        assert webhook2.last_triggered_at is not None
        assert webhook1.retry_count == 0
        assert webhook2.retry_count == 0
        
    # Test error handling for failed webhook deliveries
    with patch('src.services.webhook_service.requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        await webhook_service.trigger_webhook(mock_session, WebhookEventType.APPLICATION_SUBMITTED, {"application_id": 789})
        
        assert webhook1.retry_count == 1

def test_validate_webhook_url():
    # Create an instance of WebhookService
    webhook_service = WebhookService()
    
    # Mock the requests.head method
    with patch('src.services.webhook_service.requests.head') as mock_head:
        # Test with valid URLs (returning 200 status code)
        mock_head.return_value.status_code = 200
        assert webhook_service.validate_webhook_url("http://valid-url.com") == True
        
        # Test with invalid URLs (returning non-200 status codes)
        mock_head.return_value.status_code = 404
        assert webhook_service.validate_webhook_url("http://invalid-url.com") == False
        
        # Test with URLs that raise exceptions
        mock_head.side_effect = Exception("Connection error")
        assert webhook_service.validate_webhook_url("http://error-url.com") == False

def test_prepare_payload():
    # Create an instance of WebhookService
    webhook_service = WebhookService()
    
    # Prepare sample data for different event types
    application_data = {"application_id": 123, "status": "submitted"}
    approval_data = {"application_id": 456, "approved_by": "John Doe"}
    
    # Call prepare_payload with different event types and data
    payload1 = webhook_service.prepare_payload(WebhookEventType.APPLICATION_SUBMITTED, application_data)
    payload2 = webhook_service.prepare_payload(WebhookEventType.APPLICATION_APPROVED, approval_data)
    
    # Assert that the returned payload contains the correct event_type
    assert payload1["event_type"] == "APPLICATION_SUBMITTED"
    assert payload2["event_type"] == "APPLICATION_APPROVED"
    
    # Verify that the payload includes a timestamp
    assert "timestamp" in payload1
    assert "timestamp" in payload2
    
    # Check that the relevant data is included in the payload
    assert payload1["application_id"] == 123
    assert payload1["status"] == "submitted"
    assert payload2["application_id"] == 456
    assert payload2["approved_by"] == "John Doe"

def test_handle_webhook_response():
    # Create a mock database session
    mock_session = Mock(spec=Session)
    
    # Create sample Webhook objects
    webhook1 = Webhook(url="http://example.com/webhook1", event_type=WebhookEventType.APPLICATION_SUBMITTED)
    webhook2 = Webhook(url="http://example.com/webhook2", event_type=WebhookEventType.APPLICATION_APPROVED)
    
    # Create mock response objects with different status codes
    success_response = Mock()
    success_response.status_code = 200
    failure_response = Mock()
    failure_response.status_code = 500
    
    # Create an instance of WebhookService
    webhook_service = WebhookService()
    
    # Call handle_webhook_response with different responses and webhooks
    webhook_service.handle_webhook_response(mock_session, success_response, webhook1)
    webhook_service.handle_webhook_response(mock_session, failure_response, webhook2)
    
    # Assert that webhook status is updated correctly (last_triggered_at, retry_count)
    assert webhook1.last_triggered_at is not None
    assert webhook1.retry_count == 0
    assert webhook2.last_triggered_at is not None
    assert webhook2.retry_count == 1
    
    # Verify that the database session is called to update the webhook
    assert mock_session.add.call_count == 2
    assert mock_session.commit.call_count == 2
    
    # Check that the method returns the correct success status
    assert webhook_service.handle_webhook_response(mock_session, success_response, webhook1) == True
    assert webhook_service.handle_webhook_response(mock_session, failure_response, webhook2) == False

@pytest.mark.asyncio
async def test_retry_failed_webhooks():
    # Create a mock database session
    mock_session = Mock(spec=Session)
    
    # Create sample failed Webhook objects with different retry counts
    webhook1 = Webhook(url="http://example.com/webhook1", event_type=WebhookEventType.APPLICATION_SUBMITTED, retry_count=1)
    webhook2 = Webhook(url="http://example.com/webhook2", event_type=WebhookEventType.APPLICATION_APPROVED, retry_count=5)
    webhook3 = Webhook(url="http://example.com/webhook3", event_type=WebhookEventType.APPLICATION_REJECTED, retry_count=10)
    mock_session.query.return_value.filter.return_value.all.return_value = [webhook1, webhook2, webhook3]
    
    # Mock the requests.post method
    with patch('src.services.webhook_service.requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Create an instance of WebhookService
        webhook_service = WebhookService()
        
        # Call retry_failed_webhooks
        await webhook_service.retry_failed_webhooks(mock_session)
        
        # Assert that requests.post was called for webhooks with retry count below threshold
        assert mock_post.call_count == 2  # webhook1 and webhook2
        
        # Verify that webhook status is updated correctly after retry attempts
        assert webhook1.retry_count == 0
        assert webhook2.retry_count == 0
        assert webhook1.last_triggered_at is not None
        assert webhook2.last_triggered_at is not None
        
        # Check that webhooks exceeding retry threshold are marked as inactive
        assert webhook3.is_active == False
        
        # Ensure that the database session is called to update the webhooks
        assert mock_session.add.call_count == 3
        assert mock_session.commit.call_count == 3