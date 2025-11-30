# app/schemas/source.py
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict

from .operator import OperatorShort


class SourceBase(BaseModel):
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=100)


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    code: str | None = Field(None, max_length=100)


class SourceOut(SourceBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SourceOutShort(BaseModel):
    id: int
    name: str
    code: str

    model_config = ConfigDict(from_attributes=True)


class SourceOperatorWeightBase(BaseModel):
    operator_id: int
    weight: int = Field(..., gt=0)


class SourceOperatorWeightSet(BaseModel):
    operators: List[SourceOperatorWeightBase]


class SourceOperatorWeightOut(BaseModel):
    operator_id: int
    weight: int
    operator: Optional[OperatorShort] = None

    model_config = ConfigDict(from_attributes=True)


class SourceWithOperators(SourceOut):
    operators: List[SourceOperatorWeightOut] = []