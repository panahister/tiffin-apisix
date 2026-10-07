# Security policy

Report suspected vulnerabilities privately through
[GitHub Security Advisories](https://github.com/panahister/tiffin-apisix/security/advisories/new). Do not
publish private keys, credentials, tokens, personal data, or exploitable deployment details in an issue.

Include the affected revision/profile, prerequisites, impact, minimal reproduction, and known mitigation.
The maintainer will investigate and coordinate disclosure after a fix or mitigation is available. No
fixed response time is promised for this proof-of-concept project.

Only the latest commit on `main` is evaluated for security fixes. The `lab-only-*` value in the public
Keycloak profile is a deliberate local development credential and is unacceptable in shared or
production environments.

Consumers remain responsible for trusted TLS, private-key custody, secret rotation, distributed rate
limits, trusted-proxy configuration, WAF and abuse controls, log redaction, multi-node operation,
dependency/image scanning, monitoring, and incident response.
