from datetime import datetime, timezone

from aveniq_application.ports import Clock


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(timezone.utc)
