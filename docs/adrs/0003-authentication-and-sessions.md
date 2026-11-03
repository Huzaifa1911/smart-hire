# ADR 0003: JWT Authentication and Authorization

**Status:** Accepted approach — implementation pending.

**Purpose:** Define JWT verification, refresh tokens, role checks and membership revocation.

## Requirements

Sign in with email/password and verify email ownership before product access. Store passwords as salted password hashes.
One account can have candidate access and organization memberships. The [access rules](../architecture/problem_statement.md#access-and-privacy) define permitted operations.
IAM currently provides only the service baseline; this decision is not implemented.

## Decision

Use JWT access tokens, rotating refresh tokens and JWKS verification. Check current membership through Identity for organization operations.
Tokens are returned in response bodies and explicitly sent by the client over HTTPS.

### Login and API Requests

1. Identity checks credentials and email verification, then returns an access token and refresh token. The proposed access-token lifetime is 15 minutes.
2. The web application keeps the access token in memory and sends `Authorization: Bearer <access_token>` with protected API requests.
3. The receiving service retrieves public keys from Identity's configured JWKS address. It validates the signature, allowed algorithm, issuer, audience and expiry.
4. The service asks Identity for current organization membership and role, then checks permission for the operation and resource.

```text
Web → Service: Bearer access token
Service → Identity JWKS: public verification keys
Service → Identity: current membership and role
Service: check operation and resource access
```

No key, membership or permission caching is used. JWKS retrieval is required for each protected request. Identity holds the private signing key; services receive public keys only.
See [JWT verification guidance](https://www.rfc-editor.org/rfc/rfc8725.html).

### Refresh and Logout

The client sends the refresh token in the request body to Identity. Identity validates its record, returns a new access token and refresh token, and invalidates the previous refresh token. Detected reuse revokes the related refresh tokens.

Identity maintains refresh-token records for expiry, rotation and revocation. A separate general session record is not required.
The browser stores the refresh token persistently. After a page reload, the web application uses it to obtain a new access token. On rotation, replace the stored refresh token; on logout, remove it. Do not put tokens in URLs or logs.
See [refresh-token security guidance](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.14).

Logout revokes refresh tokens and removes the client's local tokens. A copied access JWT can remain valid until expiry unless access-token revocation is also checked. Refresh-token revocation does not remove organization membership.

## Authorization and Roles

| Access | Permitted Scope |
| --- | --- |
| Candidate access | Own profile, resumes and application status; apply to jobs. Personal access, not an organization role. |
| Recruiter membership | Permitted job, hiring and reporting operations within that organization. |
| Owner membership | Recruiter operations plus organization details, invitations, membership and ownership management. |

Identity supplies current membership information. The resource-owning service checks the action, organization and resource ownership. JWT role claims do not replace current membership checks.
For personal candidate operations, check ownership and current candidate access through Identity. Public job browsing requires no authentication.
Identity checks its own operations against its current records without calling itself over the network.

Missing or invalid access denies the operation. If required Identity checks or JWKS retrieval fail, the protected operation remains unavailable.
See [OWASP authorization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).

## Membership Revocation

Identity records membership removal. Subsequent checks refuse that organization's access while preserving the account, candidate access and other memberships.
Scheduled recruiter actions recheck permission and defer without advancing when access was removed.

Requests already in progress require coordination. An earlier successful check must not permit a protected write or private response after access is removed. The ordering protocol remains open; live membership checks alone do not solve that race.

Workers authenticate as services and retain the originating actor context where needed. Do not retain browser tokens as credentials for long-running workflows.

## Tradeoffs and Remaining Decisions

- Without caching, protected requests depend on Identity for JWKS and current access checks.
- Define refresh-token expiry and concurrent refresh handling. Browser persistence does not extend token validity; Identity enforces expiry and revocation.
- Define signing-key rotation and whether logout must immediately invalidate issued access tokens.
- Define removal ordering for in-progress operations, service-to-service authentication and password recovery.
