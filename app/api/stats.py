# app/api/stats.py
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app import crud
from app.schemas import OperatorStats

router = APIRouter()


@router.get(
    "/operators",
    response_model=List[OperatorStats],
)
def operator_stats(
    db: Session = Depends(get_db),
) -> List[OperatorStats]:
    rows = crud.get_operator_stats_rows(db)
    return [
        OperatorStats(
            operator_id=op_id,
            operator_name=name,
            total_contacts=total_contacts,
            open_contacts=open_contacts,
        )
        for (op_id, name, total_contacts, open_contacts) in rows
    ]
