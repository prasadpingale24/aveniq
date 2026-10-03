#!/usr/bin/env python3
"""Run a Playground scenario (stand-in + investigation). Used by CLI and compose smoke."""

from __future__ import annotations

import argparse
import os
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="AVENIQ Playground scenario runner")
    parser.add_argument("--scenario", default="b03", help="Scenario id (default: b03)")
    parser.add_argument(
        "--api-base",
        default=os.environ.get("AVENIQ_API_URL", "http://127.0.0.1:8000"),
    )
    parser.add_argument(
        "--standin-base",
        default=os.environ.get("CHECKOUT_STANDIN_URL", "http://127.0.0.1:8081"),
    )
    parser.add_argument("--timeout", type=float, default=float(os.environ.get("PLAYGROUND_POLL_TIMEOUT_SEC", "60")))
    args = parser.parse_args()

    from aveniq_application.playground import run_scenario
    from aveniq_application.playground.driver import PlaygroundError

    try:
        result = run_scenario(
            args.scenario,
            args.api_base,
            args.standin_base,
            poll_timeout_sec=args.timeout,
        )
    except PlaygroundError as exc:
        print(f"playground failed [{exc.code}]: {exc}", file=sys.stderr)
        return 1

    inv = result.investigation.get("investigation", {})
    rca = result.investigation.get("rca") or {}
    print(f"scenario={result.scenario_id} investigation_id={result.investigation_id} state={result.state}")
    if rca:
        print(f"rca.status={rca.get('status')} root_cause={rca.get('root_cause', '')[:120]}...")
    evidence = result.investigation.get("evidence") or []
    print(f"evidence_count={len(evidence)}")

    if result.state != "rca_candidate":
        return 1
    root = (rca.get("root_cause") or "").lower()
    if "connection pool" not in root:
        print("RCA root_cause missing expected 'connection pool' substring", file=sys.stderr)
        return 1
    if len(evidence) < 4:
        print("Expected at least 4 evidence items", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
