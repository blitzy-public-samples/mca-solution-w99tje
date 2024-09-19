from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from src.api.models.webhook import WebhookEventType

# Base schema for webhook data
class WebhookBase(BaseModel):
    url: HttpUrl
    event_type: WebhookEventType

# Schema for creating a new webhook
class WebhookCreate(WebhookBase):
    pass

# Schema for updating an existing webhook
class WebhookUpdate(BaseModel):
    url: Optional[HttpUrl] = None
    event_type: Optional[WebhookEventType] = None
    is_active: Optional[bool] = None

# Schema for webhook response data
class WebhookResponse(WebhookBase):
    id: UUID
    is_active: bool
    created_at: datetime
    last_triggered_at: Optional[datetime] = None
    retry_count: int