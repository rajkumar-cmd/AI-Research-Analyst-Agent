from app import models  # noqa: F401
from app.core.database import Base
from app.models.admin import AdminAuditLog
from app.models.research import Source


def test_day_5_tables_are_registered() -> None:
    expected_tables = {
        "users",
        "research_runs",
        "agent_steps",
        "token_usage",
        "reports",
        "sources",
        "approval_requests",
        "admin_audit_logs",
        "prompt_versions",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_reserved_metadata_columns_use_safe_model_attributes() -> None:
    assert Source.metadata_json.property.columns[0].name == "metadata"
    assert AdminAuditLog.metadata_json.property.columns[0].name == "metadata"

