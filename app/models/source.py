# app/models/source.py
from __future__ import annotations

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.db import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(100), nullable=False, unique=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    operator_weights = relationship(
        "OperatorSourceWeight",
        back_populates="source",
        cascade="all, delete-orphan",
    )

    contacts = relationship(
        "Contact",
        back_populates="source",
    )


class OperatorSourceWeight(Base):
    __tablename__ = "operator_source_weights"
    __table_args__ = (
        UniqueConstraint(
            "operator_id",
            "source_id",
            name="uq_operator_source",
        ),
    )

    id = Column(Integer, primary_key=True)

    operator_id = Column(
        Integer,
        ForeignKey("operators.id", ondelete="CASCADE"),
        nullable=False,
    )
    source_id = Column(
        Integer,
        ForeignKey("sources.id", ondelete="CASCADE"),
        nullable=False,
    )

    weight = Column(Integer, nullable=False)

    operator = relationship(
        "Operator",
        back_populates="source_weights",
    )
    source = relationship(
        "Source",
        back_populates="operator_weights",
    )
