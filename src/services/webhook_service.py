import requests
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from src.core.config import settings
from src.utils.logger import logger
from src.api.models.webhook import Webhook
from src.api.models.application import Application

class WebhookService:
    """Class for managing and triggering webhooks"""

    def __init__(self):
        """Initialize the WebhookService"""
        # Initialize any necessary configurations for webhook management
        self.max_retries = settings.WEBHOOK_MAX_RETRIES
        self.retry_interval = settings.WEBHOOK_RETRY_INTERVAL

    def trigger_webhook(self, event_type: str, payload: Dict[str, Any], db_session: Session) -> bool:
        """Trigger a webhook for a specific event"""
        # Retrieve active webhooks for the given event_type from the database
        active_webhooks = db_session.query(Webhook).filter(Webhook.event_type == event_type, Webhook.is_active == True).all()

        overall_success = True

        for webhook in active_webhooks:
            # Prepare the payload
            prepared_payload = self.prepare_payload(event_type, payload)

            # Send HTTP POST request to the webhook URL
            try:
                response = requests.post(webhook.url, json=prepared_payload, timeout=settings.WEBHOOK_TIMEOUT)
                
                # Handle the response
                success = self.handle_webhook_response(response, webhook, db_session)
                overall_success = overall_success and success
            except requests.RequestException as e:
                logger.error(f"Failed to trigger webhook {webhook.id}: {str(e)}")
                overall_success = False

        # Log the webhook triggering process
        logger.info(f"Triggered {len(active_webhooks)} webhooks for event {event_type}")

        # Return overall success status
        return overall_success

    def validate_webhook_url(self, url: str) -> bool:
        """Validate a webhook URL"""
        # Check if the URL is well-formed
        if not url.startswith(('http://', 'https://')):
            return False

        # Attempt a HEAD request to the URL
        try:
            response = requests.head(url, timeout=settings.WEBHOOK_TIMEOUT)
            # Check for successful response
            return response.status_code == 200
        except requests.RequestException:
            return False

    def prepare_payload(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the payload for a webhook"""
        # Create a base payload structure
        payload = {
            "event_type": event_type,
            "timestamp": int(time.time()),
            "data": {}
        }

        # Add relevant data based on the event_type
        if event_type == "application_submitted":
            payload["data"] = {
                "application_id": data.get("application_id"),
                "applicant_name": data.get("applicant_name"),
                "submission_date": data.get("submission_date")
            }
        elif event_type == "application_approved":
            payload["data"] = {
                "application_id": data.get("application_id"),
                "approval_date": data.get("approval_date"),
                "approved_by": data.get("approved_by")
            }
        # Add more event types as needed

        return payload

    def handle_webhook_response(self, response: requests.Response, webhook: Webhook, db_session: Session) -> bool:
        """Handle the response from a webhook request"""
        # Check the response status code
        if response.status_code in (200, 201, 202, 204):
            # If successful:
            webhook.last_triggered = int(time.time())
            webhook.retry_count = 0
            success = True
        else:
            # If failed:
            webhook.retry_count += 1
            logger.warning(f"Webhook {webhook.id} failed with status code {response.status_code}")
            success = False

        # Update webhook in the database
        db_session.add(webhook)
        db_session.commit()

        return success

    def retry_failed_webhooks(self, db_session: Session) -> None:
        """Retry failed webhook requests"""
        # Retrieve failed webhooks from the database
        failed_webhooks = db_session.query(Webhook).filter(Webhook.retry_count > 0, Webhook.is_active == True).all()

        for webhook in failed_webhooks:
            if webhook.retry_count < self.max_retries:
                # Attempt to resend the webhook
                try:
                    response = requests.post(webhook.url, json=webhook.last_payload, timeout=settings.WEBHOOK_TIMEOUT)
                    success = self.handle_webhook_response(response, webhook, db_session)
                    if success:
                        logger.info(f"Successfully retried webhook {webhook.id}")
                except requests.RequestException as e:
                    logger.error(f"Failed to retry webhook {webhook.id}: {str(e)}")
            else:
                # Mark webhook as inactive
                webhook.is_active = False
                logger.warning(f"Webhook {webhook.id} has been marked as inactive due to too many failures")

        # Commit changes to the database
        db_session.commit()

# Human tasks:
# 1. Review and adjust the webhook payload structure for different event types
# 2. Implement additional error handling and logging as needed
# 3. Consider implementing rate limiting for webhook requests
# 4. Add authentication mechanism for webhook endpoints if required
# 5. Implement a mechanism to clean up old or inactive webhooks