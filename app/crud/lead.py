# app/crud/lead.py
from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Lead


def get_lead_by_external_id(db: Session, external_id: str) -> Optional[Lead]:
    stmt = select(Lead).where(Lead.external_id == external_id)
    return db.scalars(stmt).first()


def create_lead(db: Session, *, external_id: str) -> Lead:
    lead = Lead(external_id=external_id)
    db.add(lead)
    db.flush()
    return lead


def get_or_create_lead(db: Session, external_id: str) -> Lead:
    lead = get_lead_by_external_id(db, external_id)
    if lead is not None:
        return lead
    return create_lead(db, external_id=external_id)


def get_leads(db: Session) -> List[Lead]:
    stmt = select(Lead).order_by(Lead.id)
    return list(db.scalars(stmt).all())


def get_lead(db: Session, lead_id: int) -> Optional[Lead]:
    return db.get(Lead, lead_id)
