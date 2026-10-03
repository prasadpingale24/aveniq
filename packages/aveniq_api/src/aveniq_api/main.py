import os

import uvicorn

from aveniq_api.app import create_app


def main() -> None:
    app = create_app()
    host = os.environ.get("AVENIQ_HOST", "127.0.0.1")
    port = int(os.environ.get("AVENIQ_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
