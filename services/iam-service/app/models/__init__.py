"""Import all models so Alembic sees the complete IAM metadata."""

from app.core.database import Base
from app.models.tenant import Tenant
from app.models.tenant_invitation import TenantInvitation
from app.models.tenant_membership import TenantMembership
from app.models.user import User

__all__ = ["Base", "Tenant", "TenantInvitation", "TenantMembership", "User"]
