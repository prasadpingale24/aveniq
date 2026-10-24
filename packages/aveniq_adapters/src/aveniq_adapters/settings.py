from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    aveniq_env: str = "local"
    aveniq_sqlite_path: Path = Path(".data/aveniq.db")
    fixture_root: Path = Path("fixtures")
    connector_mode: str = "fixture"
    investigation_run_enabled: bool = True
    service_name: str = "aveniq-api"
    service_version: str = "0.1.0"
    otel_exporter_otlp_endpoint: str | None = None
    checkout_standin_url: str = "http://127.0.0.1:8081"
    playground_poll_timeout_sec: float = 60.0
    playground_poll_interval_sec: float = 0.5

    auth_enabled: bool = False
    auth_session_secret: str = "dev-insecure-change-in-production"
    auth_dev_users: str = "engineer:aveniq"
    auth_cookie_name: str = "aveniq_session"
    auth_cookie_max_age_sec: int = 86_400

    def repo_root(self) -> Path:
        return Path.cwd()
