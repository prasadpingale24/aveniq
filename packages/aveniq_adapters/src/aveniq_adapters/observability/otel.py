from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from aveniq_adapters.settings import Settings

_tracer: trace.Tracer | None = None


def setup_otel(settings: Settings) -> trace.Tracer:
    global _tracer
    resource = Resource.create(
        {
            "service.name": settings.service_name,
            "service.version": settings.service_version,
            "deployment.environment": settings.aveniq_env,
        }
    )
    provider = TracerProvider(resource=resource)
    if settings.aveniq_env == "ci":
        trace.set_tracer_provider(provider)
        _tracer = trace.get_tracer("aveniq")
        return _tracer
    if settings.otel_exporter_otlp_endpoint:
        try:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

            provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
        except ImportError:
            provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    else:
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    _tracer = trace.get_tracer("aveniq")
    return _tracer


def get_tracer() -> trace.Tracer:
    if _tracer is None:
        return trace.get_tracer("aveniq")
    return _tracer
