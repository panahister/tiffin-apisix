#!/usr/bin/env python3
"""Render the tracked Tiffin APISIX template with local TLS and auth material."""

from __future__ import annotations

import argparse
import os
import pathlib
import tempfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
PROFILE = ROOT / "product/tiffin-local"


def read_required(path: pathlib.Path, label: str) -> str:
    value = path.read_text(encoding="utf-8").strip()
    if not value:
        raise ValueError(f"{label} is empty: {path}")
    return value


def payload_lines(value: str) -> str:
    return "\n".join(f"      {line}" for line in value.splitlines() if not line.startswith("#"))


def render(auth: str, certificate: pathlib.Path, private_key: pathlib.Path) -> str:
    if auth not in {"off", "keycloak"}:
        raise ValueError("auth must be off or keycloak")

    template = read_required(PROFILE / "apisix.template.yaml", "template")
    replacements = {
        "__EDGE_AUTH__": payload_lines(read_required(PROFILE / f"edge-auth.{auth}.yaml", "auth profile")),
        "__CERTIFICATE__": payload_lines(read_required(certificate, "certificate")),
        "__KEY__": payload_lines(read_required(private_key, "private key")),
    }
    for marker, value in replacements.items():
        if template.count(marker) != 1:
            raise ValueError(f"template must contain {marker} exactly once")
        template = template.replace(marker, value)
    if "__" in template:
        raise ValueError("rendered template contains an unresolved marker")
    return template.rstrip() + "\n"


def write_private(path: pathlib.Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    temporary = pathlib.Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth", choices=("off", "keycloak"), required=True)
    parser.add_argument("--certificate", type=pathlib.Path, required=True)
    parser.add_argument("--private-key", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()

    write_private(
        args.output.resolve(),
        render(args.auth, args.certificate.resolve(), args.private_key.resolve()),
    )
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
