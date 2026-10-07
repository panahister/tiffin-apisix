# Tiffin local APISIX profile

This directory is the source of truth for the Tiffin proof-of-concept gateway. The backend renders
`apisix.template.yaml` into an ignored workstation file, injecting local TLS material and one reviewed
edge-authentication profile. `config.yaml` keeps APISIX in declarative standalone mode, so the Admin API
cannot introduce route drift.

The edge exposes anonymous restaurant/menu reads and authenticated Access, Media, Restaurants, Ordering,
Kitchen, Tracking, Notifications, and unary gRPC routes. Payments remains internal-only. Each backend
validates the same bearer token independently. Optional Keycloak validation at APISIX adds a boundary; it
is never the only authorization wall.

Roles, resources, and permissions are owned by
[Tiffin Keycloak](https://github.com/panahister/tiffin-keycloak). Add or remove product routes in the
template, then run repository validation and the backend readiness/scenario suite before review.
