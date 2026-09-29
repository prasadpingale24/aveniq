from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from aveniq_application.ports import (
    ChangePort,
    DeploymentQuerySpec,
    LogQuerySpec,
    MetadataPort,
    MetricQuerySpec,
    TelemetryPort,
)


class ConnectorError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


FORBIDDEN_NAMES = ("ground_truth",)


class FixtureStore:
    def __init__(self, fixture_root: Path) -> None:
        self._root = fixture_root.resolve()

    def benchmark_dir(self, benchmark_id: str) -> Path:
        path = (self._root / benchmark_id).resolve()
        if not str(path).startswith(str(self._root)):
            raise ConnectorError("fixture_invalid", "path escape")
        if not path.is_dir():
            raise ConnectorError("fixture_not_found", benchmark_id)
        return path

    def read_json(self, benchmark_id: str, name: str) -> object:
        self._assert_allowed(name)
        path = self.benchmark_dir(benchmark_id) / name
        if not path.is_file():
            raise ConnectorError("fixture_invalid", f"missing {name}")
        return json.loads(path.read_text(encoding="utf-8"))

    def read_jsonl(self, benchmark_id: str, relative: str) -> list[dict]:
        self._assert_allowed(relative)
        path = self.benchmark_dir(benchmark_id) / relative
        if not path.is_file():
            return []
        lines = path.read_text(encoding="utf-8").strip().splitlines()
        return [json.loads(line) for line in lines if line.strip()]

    def _assert_allowed(self, name: str) -> None:
        lower = name.lower()
        for forbidden in FORBIDDEN_NAMES:
            if forbidden in lower:
                raise ConnectorError("fixture_invalid", "ground_truth access forbidden")


class FixtureMetadataPort(MetadataPort):
    def __init__(self, store: FixtureStore) -> None:
        self._store = store

    def get_alert(self, benchmark_id: str) -> dict:
        data = self._store.read_json(benchmark_id, "alert.json")
        if not isinstance(data, dict):
            raise ConnectorError("fixture_invalid", "alert.json must be object")
        return data

    def get_manifest(self, benchmark_id: str) -> dict:
        data = self._store.read_json(benchmark_id, "manifest.json")
        if not isinstance(data, dict):
            raise ConnectorError("fixture_invalid", "manifest.json must be object")
        return data

    def get_services(self, benchmark_id: str) -> list[dict]:
        data = self._store.read_json(benchmark_id, "services.json")
        if not isinstance(data, list):
            raise ConnectorError("fixture_invalid", "services.json must be array")
        return data


class FixtureTelemetryPort(TelemetryPort):
    def __init__(self, store: FixtureStore) -> None:
        self._store = store

    def query_logs(self, benchmark_id: str, spec: LogQuerySpec) -> list[dict]:
        records = self._store.read_jsonl(benchmark_id, f"logs/{spec.service}.jsonl")
        return [r for r in records if _in_window(r.get("timestamp"), spec.window)]

    def query_metrics(self, benchmark_id: str, spec: MetricQuerySpec) -> list[dict]:
        path = f"metrics/{spec.metric_name}.jsonl"
        records = self._store.read_jsonl(benchmark_id, path)
        filtered = [
            r
            for r in records
            if r.get("metric") == spec.metric_name and _in_window(r.get("timestamp"), spec.window)
        ]
        return filtered


class FixtureChangePort(ChangePort):
    def __init__(self, store: FixtureStore) -> None:
        self._store = store

    def list_deployments(self, benchmark_id: str, spec: DeploymentQuerySpec) -> list[dict]:
        data = self._store.read_json(benchmark_id, "deployments.json")
        if not isinstance(data, list):
            raise ConnectorError("fixture_invalid", "deployments.json must be array")
        result = []
        for dep in data:
            if dep.get("service") != spec.service:
                continue
            started = _parse_dt(dep.get("started_at"))
            if started and spec.window.start <= started <= spec.window.end:
                result.append(dep)
        return result


def _parse_dt(value: object) -> datetime | None:
    if value is None:
        return None
    text = str(value).replace("Z", "+00:00")
    dt = datetime.fromisoformat(text)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _in_window(value: object, window) -> bool:
    dt = _parse_dt(value)
    if dt is None:
        return False
    return window.start <= dt <= window.end
