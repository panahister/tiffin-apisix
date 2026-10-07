# Contributing

Changes must keep the gateway declarative, reviewable, and secondary to backend authorization.

Before opening a pull request:

```bash
python3 -m unittest discover -s tests -v
```

Render both `off` and `keycloak` profiles, validate them with the pinned APISIX image, and run the backend
readiness plus business scenario suite for route changes. Add a regression for defects. Document public
surface, priority, method, rate-limit, identity, and internal-service impact.

Never commit TLS private keys, rendered `apisix.yaml`, production secrets, access tokens, personal data,
or private network addresses. Follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and report vulnerabilities
through [SECURITY.md](SECURITY.md).
