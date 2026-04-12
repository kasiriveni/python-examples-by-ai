"""
This script demonstrates structured logging with structlog and tracing with OpenTelemetry.
Topics covered:
1. Setting up structlog for structured logging.
2. Integrating OpenTelemetry for distributed tracing.
"""

import structlog
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.console.span import ConsoleSpanExporter

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()

# Configure OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Example usage
logger.info("Application started", event="startup")

with tracer.start_as_current_span("example-span"):
    logger.info("Processing task", task_id=123)

logger.info("Application finished", event="shutdown")