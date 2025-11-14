from sqlalchemy import text

NEW_COLUMNS = [
    ("reference_number", "TEXT", "NULL"),
    ("complaint_type", "TEXT", "''"),
    ("main_category", "TEXT", "''"),
    ("fraud_type", "TEXT", "''"),
    ("sub_type", "TEXT", "''"),
    ("name", "TEXT", "''"),
    ("father_spouse_guardian_name", "TEXT", "''"),
    ("date_of_birth", "TEXT", "''"),
    ("phone_number", "TEXT", "''"),
    ("email_id", "TEXT", "''"),
    ("gender", "TEXT", "''"),
    ("village", "TEXT", "''"),
    ("post_office", "TEXT", "''"),
    ("police_station", "TEXT", "''"),
    ("district", "TEXT", "''"),
    ("pin_code", "TEXT", "''"),
    ("documents", "TEXT", "'[]'"),
    ("account_number", "TEXT", "''"),
    ("acknowledgement_number", "TEXT", "''"),
    ("updated_at", "DATETIME", "''"),
]


def ensure_schema(engine):
    """Add newly introduced columns if they are missing (simple sqlite migration)."""
    with engine.connect() as conn:
        result = conn.execute(text("PRAGMA table_info('complaints');"))
        existing_columns = {row[1] for row in result}

        columns_after_execution = set(existing_columns)

        for column_name, column_type, default_value in NEW_COLUMNS:
            if column_name in existing_columns:
                columns_after_execution.add(column_name)
                continue

            if default_value == "NULL":
                default_clause = ""
            else:
                default_clause = f"DEFAULT {default_value}"

            conn.execute(
                text(
                    f"ALTER TABLE complaints "
                    f"ADD COLUMN {column_name} {column_type} {default_clause}"
                )
            )
            columns_after_execution.add(column_name)

        # Backfill updated_at where empty
        if "updated_at" in columns_after_execution:
            conn.execute(
                text(
                    "UPDATE complaints SET updated_at = COALESCE(updated_at, created_at) "
                    "WHERE updated_at IS NULL OR updated_at = ''"
                )
            )

