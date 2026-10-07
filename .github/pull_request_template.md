## Edge change

Describe the route, method, protocol, upstream, priority, plugin, and public-surface impact.

## Security impact

Describe authentication, backend authorization, rate limit, request identity, TLS, and internal-service impact.

## Evidence

- [ ] `python3 -m unittest discover -s tests -v`
- [ ] Both edge-auth profiles render
- [ ] Pinned APISIX image validates the generated file
- [ ] Backend readiness and relevant business scenarios pass
- [ ] No private key, credential, token, personal data, or production network detail is included

## Limits

State what this change does not prove or support.
