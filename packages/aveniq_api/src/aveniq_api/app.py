import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from aveniq_adapters.factory import AppServices, connect, migrate
from aveniq_adapters.observability.otel import setup_otel
from aveniq_adapters.settings import Settings

from aveniq_api.errors import register_exception_handlers
from aveniq_api.playground_routes import router as playground_router
from aveniq_api.routes import router


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        migrate(settings.aveniq_sqlite_path)
        conn = connect(settings.aveniq_sqlite_path)
        app.state.settings = settings
        app.state.services = AppServices(settings, conn)
        app.state.db_conn = conn
        setup_otel(settings)
        yield
        conn.close()

    app = FastAPI(
        title="AVENIQ Investigation API",
        version="0.1.0",
        description=(
            "Evidence-first incident investigations (Phase 0b–1). "
            "Try **POST /api/v1/investigations** with example **b03_alert**, "
            "then **POST .../run**, then **GET** by id. "
            "Contract source: engineering/api/openapi.yaml"
        ),
        lifespan=lifespan,
    )
    register_exception_handlers(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    app.include_router(playground_router)
    return app
