"""Allowed values for IAM lifecycle states and organization roles."""

from enum import StrEnum


class UserStatus(StrEnum):
    ACTIVE = "active"
    DISABLED = "disabled"


class TenantStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class MembershipRole(StrEnum):
    OWNER = "owner"
    RECRUITER = "recruiter"


class MembershipStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class InvitationStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REVOKED = "revoked"
    EXPIRED = "expired"
