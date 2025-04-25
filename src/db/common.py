from sqlmodel import Column, DateTime, Field, create_engine, func

from src.settings import POSTGRES_URL


def created_at() -> Field:
    """Returns auto-updating non-null created_at field."""
    return Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )


def updated_at() -> Field:
    """Returns auto-updating non-null updated_at field."""
    return Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )


engine = create_engine(POSTGRES_URL)
