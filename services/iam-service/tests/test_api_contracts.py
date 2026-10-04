"""Contract validation and honest placeholder behavior for IAM endpoints."""

import pytest
from pydantic import ValidationError

from app.core.enums import MembershipRole
from app.schemas.auth import CandidateSignupRequest
from app.schemas.tenants import MembershipUpdateRequest, TenantCreateRequest

TENANT = "00000000-0000-0000-0000-000000000001"
MEMBERSHIP = "00000000-0000-0000-0000-000000000002"
INVITATION = "00000000-0000-0000-0000-000000000003"
ACCOUNT = {"email": "alice@example.com", "password": "test-password", "full_name": "Alice"}


@pytest.mark.parametrize(
    ("method", "path", "body"),
    [
        ("POST", "/auth/candidate-signup", ACCOUNT),
        (
            "POST",
            "/auth/organization-signup",
            {**ACCOUNT, "organization": {"name": "Acme", "slug": "acme"}},
        ),
        ("POST", "/auth/login", {"email": ACCOUNT["email"], "password": ACCOUNT["password"]}),
        ("GET", "/users/me", None),
        ("PATCH", "/users/me", {"full_name": "Alice Updated"}),
        ("PUT", "/users/me/candidate-access", None),
        ("GET", "/users/me/memberships", None),
        ("POST", "/tenants", {"name": "Acme", "slug": "acme"}),
        ("GET", f"/tenants/{TENANT}", None),
        ("PATCH", f"/tenants/{TENANT}", {"name": "Acme Updated"}),
        ("GET", f"/tenants/{TENANT}/memberships", None),
        ("PATCH", f"/tenants/{TENANT}/memberships/{MEMBERSHIP}", {"role": "owner"}),
        ("POST", f"/tenants/{TENANT}/invitations", {"email": "bob@example.com"}),
        ("GET", f"/tenants/{TENANT}/invitations", None),
        ("POST", f"/tenants/{TENANT}/invitations/{INVITATION}/revoke", None),
        ("POST", "/invitations/accept", {"token": "secret-invitation-token"}),
    ],
)
def test_declared_endpoints_do_not_claim_implementation(client, method, path, body):
    response = client.request(method, f"/iam-service/v1{path}", json=body)
    assert response.status_code == 501
    assert response.json() == {"error": "This endpoint is not implemented yet"}


def test_membership_update_requires_non_null_changes():
    assert MembershipUpdateRequest(role="owner").role is MembershipRole.OWNER
    for body in [{}, {"role": None}, {"status": "unknown"}]:
        with pytest.raises(ValidationError):
            MembershipUpdateRequest.model_validate(body)


def test_signup_does_not_allow_privilege_fields():
    with pytest.raises(ValidationError):
        CandidateSignupRequest.model_validate({**ACCOUNT, "role": "owner"})
    assert ACCOUNT["password"] not in repr(CandidateSignupRequest.model_validate(ACCOUNT))


def test_subdomain_slug_validation():
    assert TenantCreateRequest(name="Acme", slug="acme-inc").slug == "acme-inc"
    for slug in ["admin", "Acme", "acme company", "-acme", "acme-", "a" * 64]:
        with pytest.raises(ValidationError):
            TenantCreateRequest(name="Acme", slug=slug)


def test_openapi_publishes_contracts_without_secrets(client):
    document = client.get("/iam-service/v1/openapi.json").json()
    signup = document["paths"]["/iam-service/v1/auth/candidate-signup"]["post"]
    assert "201" in signup["responses"] and "501" in signup["responses"]
    invitation = document["components"]["schemas"]["InvitationResponse"]["properties"]
    user = document["components"]["schemas"]["UserResponse"]["properties"]
    assert "token_hash" not in invitation
    assert "password_hash" not in user


def test_list_pagination_is_bounded(client):
    response = client.get("/iam-service/v1/users/me/memberships?limit=101")
    assert response.status_code == 422
