# Mini CRM: распределение лидов между операторами

## Запуск проекта

### Локально

1. Установить зависимости (через uv):
   uv sync

2. Запустить приложение:
   uv run uvicorn app.main:app --reload

Приложение будет доступно по адресу:
- Swagger UI: http://localhost:8000/docs
- Health-check: http://localhost:8000/health

### Через Docker

1. Собрать и запустить:
   uv run invoke docker-build

2. Поднять в фоне:
   uv run invoke docker-up

3. Остановить:
   uv run invoke docker-down


## Модель данных

Используется SQLite и SQLAlchemy. Основные сущности:

- Operator
  - Оператор, обрабатывающий обращения.
  - Поля: id, name, is_active, max_active_contacts, created_at.
  - Связи:
    - source_weights: список OperatorSourceWeight.
    - contacts: список Contact.

- Source
  - Источник (бот/канал), откуда приходят обращения.
  - Поля: id, name, code, created_at.
  - Связи:
    - operator_weights: список OperatorSourceWeight (конфигурация распределения).
    - contacts: список Contact.

- OperatorSourceWeight
  - Связка оператор ↔ источник с числовым весом.
  - Поля: id, operator_id, source_id, weight.
  - Ограничение: уникальная пара (operator_id, source_id).
  - Связи:
    - operator: Operator.
    - source: Source.

- Lead
  - Лид (конечный клиент).
  - Поля: id, external_id, created_at.
  - external_id — уникальный внешний идентификатор лида.
  - Связи:
    - contacts: список Contact.

- Contact
  - Обращение лида из конкретного источника.
  - Поля: id, lead_id, source_id, operator_id (nullable), status (open/closed), payload, created_at.
  - Связи:
    - lead: Lead.
    - source: Source.
    - operator: Operator.
  - Нагрузка оператора считается как количество открытых Contact (status = "open") для этого оператора.


## Алгоритм распределения обращений

### Определение лида

При регистрации обращения (POST /api/contacts):

- Вход содержит поле external_lead_id.
- Система ищет Lead по Lead.external_id = external_lead_id.
- Если лид найден — используется существующий Lead.
- Если не найден — создаётся новый Lead с этим external_id.

Таким образом, все обращения с одинаковым external_lead_id считаются принадлежащими одному и тому же лиду.


### Учет весов операторов по источникам

Для источника Source(id = source_id):

- Из таблицы OperatorSourceWeight выбираются все записи с данным source_id.
- Для каждой записи используется поле weight как числовой вес.
- Из операторов, прошедших фильтрацию по активности и лимиту нагрузки (см. ниже), выполняется взвешенный случайный выбор:
  - вероятность выбора оператора = weight / сумма всех weight среди подходящих операторов.
- Реализация использует стандартный random.choices с переданными весами.


### Учет лимитов нагрузки

Нагрузка оператора определяется как количество открытых обращений:

- Для каждого оператора считается:
  - active_count = количество Contact, где:
    - Contact.operator_id = id оператора
    - Contact.status = "open"
- Оператор считается доступным для новых обращений, если:
  - operator.is_active = True
  - active_count < operator.max_active_contacts

Алгоритм фильтрации:

1. Для всех OperatorSourceWeight по источнику берётся связанный Operator.
2. Из списка исключаются:
   - неактивные операторы (is_active = False),
   - операторы, у которых active_count >= max_active_contacts.
3. Взвешенный выбор выполняется только среди оставшихся операторов.


### Если подходящих операторов нет

Если после применения всех условий (активность и лимит нагрузки) не остаётся ни одного подходящего оператора:

- Оператор не назначается (operator_id = null).
- Обращение Contact всё равно создаётся и сохраняется:
  - привязано к лиду (Lead),
  - привязано к источнику (Source),
  - поле operator_id = null.

Это поведение позволяет:
- не терять обращения,
- явно видеть обращения без назначенного оператора (например, для последующей ручной обработки).

Данное поведение описано и реализовано в бизнес-логике сервиса register_contact.
