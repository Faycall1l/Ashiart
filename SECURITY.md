# Security Policy

## Supported versions

Only the latest release receives fixes. Pin to a release tag or
`pip install ashiart==<version>` rather than tracking `main`.

| Version | Supported |
| ------- | --------- |
| latest release | Yes |
| older releases | No |

## Reporting a vulnerability

Open a [private security advisory](https://github.com/Faycall1l/Ashiart/security/advisories/new)
— do not file a public issue. Include:

- Affected version and install method
- Minimal reproduction (commands plus input)
- Impact assessment if known

Expect an initial response within 7 days. Fixes ship in the next
patch release with credit unless you ask otherwise.

## Scope notes

AshiArt downloads remote images on request (`http(s)` input). Only
convert URLs you trust; responses are size-unbounded by default.
