# app/api/contact.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.services import register_contact
from app.schemas import ContactCreate, ContactOut

router = APIRouter()


@router.post(
    "/",
    response_model=ContactOut,
    status_code=status.HTTP_201_CREATED,
)
def create_contact_endpoint(
    data: ContactCreate,
    db: Session = Depends(get_db),
) -> ContactOut:
    """
    Регистрация обращения

    Внутри:
      найти/создать лида по external_lead_id
      подобрать оператора по правилам
      создать обращение

    Если подходящих операторов нет создаётся обращение без оператора
    """
    try:
        contact = register_contact(db, data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    db.commit()
    db.refresh(contact)
    return ContactOut.model_validate(contact)
