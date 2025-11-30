# app/crud/contact.py
from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Contact, ContactStatus


def create_contact(
    db: Session,
    *,
    lead_id: int,
    source_id: int,
    operator_id: int | None,
    payload: str | None = None,
    status: ContactStatus = ContactStatus.OPEN,
) -> Contact:
    contact = Contact(
        lead_id=lead_id,
        source_id=source_id,
        operator_id=operator_id,
        payload=payload,
        status=status,
    )
    db.add(contact)
    db.flush()
    return contact


def get_contacts_for_lead(db: Session, lead_id: int) -> List[Contact]:
    stmt = (
        select(Contact)
        .where(Contact.lead_id == lead_id)
        .order_by(Contact.created_at)
    )
    return list(db.scalars(stmt).all())
