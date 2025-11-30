# app/models/operator.py
from __future__ import annotations

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.db import Base


class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    is_active = Column(Boolean, nullable=False, default=True, server_default="1")
    max_active_contacts = Column(
        Integer,
        nullable=False,
        default=10,
        server_default="10",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    source_weights = relationship(
        "OperatorSourceWeight",
        back_populates="operator",
        cascade="all, delete-orphan",
    )

    contacts = relationship(
        "Contact",
        back_populates="operator",
    )
