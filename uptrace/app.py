import demo
import os
import time
import grpc
import celery


from opentelemetry.instrumentation.pymongo import PymongoInstrumentor

from opentelemetry import trace, metrics
from opentelemetry.sdk import metrics as sdkmetrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    AggregationTemporality,
    PeriodicExportingMetricReader,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter,
)

from opentelemetry.instrumentation.flask import FlaskInstrumentor

from random import randint
from flask import Flask, request, Response, make_response
from flask_mongoengine import MongoEngine

from demo import endpoints

resource = Resource(
    attributes={"service.name": "myservice", "service.version": "1.0.0"}
)

# Trace
tracer_provider = TracerProvider(
    resource=resource,
)
trace.set_tracer_provider(tracer_provider)

exporter = OTLPSpanExporter(
    endpoint="http://otelcol:4317",
    # Set the Uptrace dsn here or use UPTRACE_DSN env var.
    # headers=(("uptrace-dsn", dsn),),
    timeout=5,
    compression=grpc.Compression.Gzip,
)

span_processor = BatchSpanProcessor(
    exporter,
    max_queue_size=1000,
    max_export_batch_size=1000,
)
tracer_provider.add_span_processor(span_processor)
tracer = trace.get_tracer("app_or_package_name", "1.0.0")


# Metrix
temporality_delta = {
    sdkmetrics.Counter: AggregationTemporality.DELTA,
    sdkmetrics.UpDownCounter: AggregationTemporality.DELTA,
    sdkmetrics.Histogram: AggregationTemporality.DELTA,
    sdkmetrics.ObservableCounter: AggregationTemporality.DELTA,
    sdkmetrics.ObservableUpDownCounter: AggregationTemporality.DELTA,
    sdkmetrics.ObservableGauge: AggregationTemporality.DELTA,
}

metric_exporter = OTLPMetricExporter(
    endpoint="http://otelcol:4317",
    # headers=(("uptrace-dsn", dsn),),
    timeout=5,
    compression=grpc.Compression.Gzip,
    preferred_temporality=temporality_delta,
)
reader = PeriodicExportingMetricReader(metric_exporter)
provider = MeterProvider(metric_readers=[reader], resource=resource)
metrics.set_meter_provider(provider)
meter = metrics.get_meter("github.com/uptrace/uptrace-python", "1.0.0")
counter = meter.create_counter("some.prefix.counter", description="TODO")


app = demo.create_app()

app.register_blueprint(endpoints.app)
celery_app = demo.celery_init_app(app)

FlaskInstrumentor().instrument_app(app)

