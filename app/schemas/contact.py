# app/schemas/contact.py
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.models import ContactStatus
from .operator import OperatorShort


class ContactBase(BaseModel):
    payload: Optional[str] = None


class ContactCreate(BaseModel):
    external_lead_id: str = Field(..., max_length=255)
    source_id: int
    payload: Optional[str] = None


class ContactOut(BaseModel):
    id: int
    lead_id: int
    source_id: int
    operator_id: Optional[int] = None
    status: ContactStatus
    payload: Optional[str] = None
    created_at: datetime

    operator: Optional[OperatorShort] = None

    model_config = ConfigDict(from_attributes=True)
