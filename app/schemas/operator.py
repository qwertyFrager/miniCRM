# app/schemas/operator.py
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class OperatorBase(BaseModel):
    name: str = Field(..., max_length=255)
    is_active: bool = True
    max_active_contacts: int = Field(10, ge=0)


class OperatorCreate(OperatorBase):
    pass


class OperatorUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    is_active: bool | None = None
    max_active_contacts: int | None = Field(None, ge=0)


class OperatorOut(OperatorBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OperatorShort(BaseModel):
    id: int
    name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class OperatorStats(BaseModel):
    operator_id: int
    operator_name: str
    total_contacts: int
    open_contacts: int
