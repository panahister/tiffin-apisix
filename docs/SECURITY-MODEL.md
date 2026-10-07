# Security model

## Trust boundaries

- The client is untrusted.
- APISIX is an edge routing and optional authentication layer, not the sole authorization authority.
- Every backend validates token signature, issuer, audience, role, tenant, and domain policy.
- Service-to-service-only APIs have no public route.
- TLS private keys and rendered configuration are local secret-bearing output.

## Authentication profiles

### `off`

APISIX forwards the bearer token unchanged. The backend remains fully responsible for validation. This
profile is useful to prove that the service boundary is not accidentally dependent on edge enforcement.

### `keycloak`

APISIX discovers the Tiffin realm and validates bearer tokens from cached public keys. It does not call
Keycloak for every request and does not inject access-token, ID-token, or user-info headers. The backend
still validates the forwarded bearer token.

## Anonymous surface

Only restaurant/menu GET requests are anonymous. They receive a bounded per-address local rate limit.
The higher-priority route is method-constrained so protected restaurant mutations cannot match it.

## Request identity

The global `request-id` plugin creates or propagates `X-Request-Id` and returns it in the response. Domain
services use correlation for logs and failures. A request ID is not an identity or authorization claim.

## Production checklist

- Replace local certificates with automated trusted certificates and rotation.
- Remove public development secrets and use managed secret custody.
- Select distributed rate-limit storage for multiple APISIX nodes.
- Define trusted proxy and real client-address handling before using address-based policy.
- Add access-log redaction, retention, metrics, traces, alerts, and incident procedures.
- Review OIDC discovery/JWKS cache and failure behavior.
- Add WAF, bot, abuse, and DDoS controls appropriate to the deployment.
- Validate route/schema changes before a staged, observable rollout.
- Run load, failover, and certificate-rotation acceptance.

A successful local route check does not satisfy this production checklist.
