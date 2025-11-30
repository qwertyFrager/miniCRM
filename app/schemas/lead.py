# app/schemas/lead.py
from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict

from .contact import ContactOut


class LeadBase(BaseModel):
    external_id: str = Field(..., max_length=255)


class LeadCreate(LeadBase):
    pass


class LeadOut(LeadBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LeadWithContacts(LeadOut):
    contacts: List[ContactOut] = []