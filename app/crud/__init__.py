# app/crud/__init__.py
from .operator import (
    get_operators,
    get_operator,
    create_operator,
    update_operator,
    get_operator_active_contacts_count,
    get_operator_stats_rows,
)
from .source import (
    get_sources,
    get_source,
    get_source_by_code,
    create_source,
    update_source,
    set_source_operator_weights,
    get_weights_for_source,
)
from .lead import (
    get_lead_by_external_id,
    create_lead,
    get_or_create_lead,
    get_leads,
    get_lead,
)
from .contact import (
    create_contact,
    get_contacts_for_lead,
)

__all__ = [
    # operator
    "get_operators",
    "get_operator",
    "create_operator",
    "update_operator",
    "get_operator_active_contacts_count",
    "get_operator_stats_rows",
    # source
    "get_sources",
    "get_source",
    "get_source_by_code",
    "create_source",
    "update_source",
    "set_source_operator_weights",
    "get_weights_for_source",
    # lead
    "get_lead_by_external_id",
    "create_lead",
    "get_or_create_lead",
    "get_leads",
    "get_lead",
    # contact
    "create_contact",
    "get_contacts_for_lead",
]
