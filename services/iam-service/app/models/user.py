"""Global account; candidate capability is independent of memberships."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Index, Text, false, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.enums import UserStatus
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.tenant_membership import TenantMembership


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("btrim(email) <> ''", name="ck_users_email_nonempty"),
        CheckConstraint("btrim(full_name) <> ''", name="ck_users_full_name_nonempty"),
    )
    email: Mapped[str] = mapped_column(Text)
    password_hash: Mapped[str] = mapped_column(Text)
    full_name: Mapped[str] = mapped_column(Text)
    status: Mapped[UserStatus] = mapped_column(
        SAEnum(
            UserStatus,
            name="user_status",
            values_callable=lambda enum: [member.value for member in enum],
            native_enum=True,
            validate_strings=True,
        ),
        default=UserStatus.ACTIVE,
        server_default=UserStatus.ACTIVE.value,
    )
    is_candidate: Mapped[bool] = mapped_column(Boolean, default=False, server_default=false())
    memberships: Mapped[list["TenantMembership"]] = relationship(
        back_populates="user", passive_deletes="all"
    )


Index("users_email_ci_uq", func.lower(func.btrim(User.email)), unique=True)
