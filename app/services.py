# app/services.py
from __future__ import annotations

import random
from typing import List, Optional, Sequence, Tuple

from sqlalchemy.orm import Session

from app.models import Operator, Contact
from app.schemas import ContactCreate
from app.crud import (
    get_or_create_lead,
    get_source,
    get_weights_for_source,
    get_operator_active_contacts_count,
    create_contact,
)


def _choose_operator_weighted(
    candidates: Sequence[Tuple[Operator, int]],
) -> Optional[Operator]:
    """
    Взвешенный случайный выбор оператора
    candidates: список кортежей (operator, weight)
    """
    if not candidates:
        return None

    operators, weights = zip(*candidates)
    # стандартный взвешенный рандом из stdlib
    chosen = random.choices(list(operators), weights=list(weights), k=1)[0]
    return chosen


def assign_operator_for_source(
    db: Session,
    *,
    source_id: int,
) -> Optional[Operator]:
    """
    Выбор оператора для данного источника с учетом:
      активности оператора (is_active)
      не превышенного лимита нагрузки (max_active_contacts)
      весов для источника

    Если подходящих операторов нет возвращает None
    """
    weights = get_weights_for_source(db, source_id=source_id)

    candidates: List[Tuple[Operator, int]] = []

    for w in weights:
        operator = w.operator  # lazy-load, но операторов мало, это ок
        if operator is None:
            continue

        if not operator.is_active:
            continue

        active_count = get_operator_active_contacts_count(db, operator.id)
        if active_count >= operator.max_active_contacts:
            # оператор перегружен
            continue

        candidates.append((operator, w.weight))

    if not candidates:
        return None

    return _choose_operator_weighted(candidates)


def register_contact(
    db: Session,
    data: ContactCreate,
) -> Contact:
    """
    Высокоуровневая операция регистрации обращения:

    1) Найти или создать лида по external_lead_id
    2) Проверить, что источник существует
    3) Подобрать оператора по правилам
    4) Создать обращение

    ВАЖНО: если подходящих операторов нет, мы создаём обращение
    с operator_id = None (без оператора)
    """
    # 1. Лид
    lead = get_or_create_lead(db, external_id=data.external_lead_id)

    # 2. Источник
    source = get_source(db, data.source_id)
    if source is None:
        # В API преобразуем это в HTTPException(404)
        raise ValueError(f"Source {data.source_id} not found")

    # 3. Подбор оператора
    operator = assign_operator_for_source(db, source_id=source.id)
    operator_id: Optional[int] = operator.id if operator is not None else None

    # 4. Создание обращения
    contact = create_contact(
        db,
        lead_id=lead.id,
        source_id=source.id,
        operator_id=operator_id,
        payload=data.payload,
    )

    return contact
