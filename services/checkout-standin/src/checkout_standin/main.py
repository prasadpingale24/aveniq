from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field

import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

logger = logging.getLogger("checkout-standin")
logging.basicConfig(level=logging.INFO, format="%(message)s")

app = FastAPI(title="checkout-api stand-in", version="0.1.0")


@dataclass
class StandinState:
    scenario_active: bool = False
    trigger_count: int = 0
    pool_max_size: int = 50
    pool_in_use: int = 2
    error_rate: float = 0.01
    log_lines: list[str] = field(default_factory=list)


state = StandinState()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "checkout-api-standin"}


@app.post("/playground/reset")
def playground_reset() -> dict[str, str]:
    state.scenario_active = False
    state.trigger_count = 0
    state.pool_max_size = 50
    state.pool_in_use = 2
    state.error_rate = 0.01
    state.log_lines.clear()
    logger.info("playground reset: checkout-api stand-in idle")
    return {"status": "reset"}


@app.post("/playground/scenarios/b03/trigger")
def trigger_b03() -> dict[str, object]:
    state.scenario_active = True
    state.trigger_count += 1
    state.pool_max_size = 5
    state.pool_in_use = 5
    state.error_rate = 0.42
    messages = [
        "deployment applied version=2.8.1 config database.pool.max_size=5",
        "WARN checkout-api database connection pool exhausted waiting for connection",
        "ERROR checkout-api HikariPool - Connection is not available, request timed out after 30000ms",
        "ERROR checkout-api checkout failed: could not acquire connection from pool",
    ]
    for msg in messages:
        state.log_lines.append(msg)
        logger.error(msg)
    return {
        "status": "triggered",
        "scenario": "b03",
        "service": "checkout-api",
        "deployment_version": "2.8.1",
        "pool_max_size": state.pool_max_size,
    }


@app.get("/playground/logs")
def playground_logs() -> dict[str, list[str]]:
    return {"lines": list(state.log_lines)}


@app.get("/metrics")
def metrics() -> PlainTextResponse:
    lines = [
        "# HELP checkout_db_pool_max Maximum pool size",
        "# TYPE checkout_db_pool_max gauge",
        f"checkout_db_pool_max {state.pool_max_size}",
        "# HELP checkout_db_pool_in_use Connections in use",
        "# TYPE checkout_db_pool_in_use gauge",
        f"checkout_db_pool_in_use {state.pool_in_use}",
        "# HELP checkout_error_rate Error rate ratio",
        "# TYPE checkout_error_rate gauge",
        f"checkout_error_rate {state.error_rate}",
    ]
    return PlainTextResponse("\n".join(lines) + "\n", media_type="text/plain; version=0.0.4")


def main() -> None:
    host = os.environ.get("CHECKOUT_STANDIN_HOST", "0.0.0.0")
    port = int(os.environ.get("CHECKOUT_STANDIN_PORT", "8081"))
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
