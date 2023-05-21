import os
import sentry_sdk
import sentry_sdk.integrations.flask

from flask import Flask, request, current_app


from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor


from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "nino-flask"
})


# Matrix
reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://otelcol:4317")
)
meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meter_provider)

# Trace
trace_provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    ConsoleSpanExporter()
)
trace_provider.add_span_processor(processor)
trace.set_tracer_provider(trace_provider)


app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/", methods={'POST'})
def hello_world():
    return "<p>Hello, World!</p>"


