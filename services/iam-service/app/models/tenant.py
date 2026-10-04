"""Organization and its memberships; users themselves are global."""

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.enums import TenantStatus
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.tenant_membership import TenantMembership


class Tenant(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "tenants"
    __table_args__ = (
        CheckConstraint("btrim(name) <> ''", name="ck_tenants_name_nonempty"),
        CheckConstraint("slug = lower(slug) AND btrim(slug) <> ''", name="ck_tenants_slug"),
    )
    name: Mapped[str] = mapped_column(Text)
    slug: Mapped[str] = mapped_column(Text, unique=True)
    status: Mapped[TenantStatus] = mapped_column(
        SAEnum(
            TenantStatus,
            name="tenant_status",
            values_callable=lambda enum: [member.value for member in enum],
            native_enum=True,
            validate_strings=True,
        ),
        default=TenantStatus.ACTIVE,
        server_default=TenantStatus.ACTIVE.value,
    )
    memberships: Mapped[list["TenantMembership"]] = relationship(
        back_populates="tenant", passive_deletes="all"
    )
