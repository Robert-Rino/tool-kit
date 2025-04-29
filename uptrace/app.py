import demo
import os
import celery

import opentelemetry
import opentelemetry.exporter.otlp.proto.grpc.metric_exporter
import opentelemetry.exporter.otlp.proto.grpc.trace_exporter
import opentelemetry.instrumentation.wsgi
import opentelemetry.sdk.metrics
import opentelemetry.sdk.trace
import opentelemetry.sdk.trace.export
import opentelemetry.semconv.trace
import pkg_resources


tracer = opentelemetry.sdk.trace.TracerProvider()
tracer.add_span_processor(
    opentelemetry.sdk.trace.export.BatchSpanProcessor(
        opentelemetry.exporter.otlp.proto.grpc.trace_exporter.OTLPSpanExporter(),
    ),
)
opentelemetry.trace.set_tracer_provider(tracer)

meter = opentelemetry.sdk.metrics.MeterProvider([
    opentelemetry.sdk.metrics.export.PeriodicExportingMetricReader(
        opentelemetry.exporter.otlp.proto.grpc.metric_exporter.OTLPMetricExporter()
    )
])
opentelemetry.metrics.set_meter_provider(meter)

for entry_point in pkg_resources.iter_entry_points('opentelemetry_instrumentor'):
    Instrumentor = entry_point.load()
    Instrumentor().instrument()

app = demo.create_app()

# app.register_blueprint(demo.endpoints.app)
celery_app = demo.celery_init_app(app)

