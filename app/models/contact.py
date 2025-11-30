# app/models/contact.py
from __future__ import annotations

import enum

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.db import Base


class ContactStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"


class Contact(Base):
    __tablename__ = "contacts"
    __table_args__ = (
        Index(
            "ix_contacts_operator_status",
            "operator_id",
            "status",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    lead_id = Column(
        Integer,
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
    )
    source_id = Column(
        Integer,
        ForeignKey("sources.id", ondelete="RESTRICT"),
        nullable=False,
    )
    operator_id = Column(
        Integer,
        ForeignKey("operators.id", ondelete="SET NULL"),
        nullable=True,
    )

    status = Column(
        Enum(ContactStatus, native_enum=False),
        nullable=False,
        default=ContactStatus.OPEN,
        server_default=ContactStatus.OPEN.value,
    )

    payload = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    lead = relationship(
        "Lead",
        back_populates="contacts",
    )
    source = relationship(
        "Source",
        back_populates="contacts",
    )
    operator = relationship(
        "Operator",
        back_populates="contacts",
    )
