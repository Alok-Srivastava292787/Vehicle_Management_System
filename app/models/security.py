from datetime import datetime

from sqlalchemy import (
    BIGINT,
    BOOLEAN,
    TIMESTAMP,
    VARCHAR,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base import Base


class User(Base):

    __tablename__ = "users"
    __table_args__ = {
        "schema": "security"
    }

    user_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
    )

    employee_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "master.employee_master.employee_id"
        ),
        nullable=True,
    )
    username: Mapped[str] = mapped_column(
        VARCHAR(100),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        VARCHAR,
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        VARCHAR(200),
        nullable=True,
    )

    active_flag: Mapped[bool] = mapped_column(
        BOOLEAN,
        default=True,
    )

    last_login: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        nullable=True,
    )

    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        nullable=True,
    )
class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {
        "schema": "security"
    }
    role_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
    )
    role_name: Mapped[str] = mapped_column(
        VARCHAR(100),
        unique=True,
        nullable=False,
    )
    active_flag: Mapped[bool] = mapped_column(
        BOOLEAN,
        default=True,
    )

class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = {
        "schema": "security"
    }
    user_role_id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "security.users.user_id"
        )
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey(
            "security.roles.role_id"
        )
    )
