import time
import uuid


def new_ulid() -> str:
    """Generate a sortable id (UUID v7 when available, else uuid4)."""
    if hasattr(uuid, "uuid7"):
        return str(uuid.uuid7())
    return str(uuid.uuid4())


def monotonic_ms() -> int:
    return int(time.time() * 1000)
