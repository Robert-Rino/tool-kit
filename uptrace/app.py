import os
import time

import grpc

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
from flask import Flask

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


app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/rolldice")
def roll_dice():
    counter.add(1)
    return str(do_roll())

def do_roll():
    with tracer.start_as_current_span("main") as rollspan:
        trace_id = rollspan.get_span_context().trace_id
        print(f"trace id: {trace_id:0{32}x}")
        res = randint(1, 6)
        rollspan.set_attribute("roll.value", res)
        # This adds 1 to the counter for the given roll value
        # roll_counter.add(1, {"roll.value": res})
        return res


# import os
# import sentry_sdk
# import sentry_sdk.integrations.flask

# from flask import Flask, request, current_app
# from random import randint


# from opentelemetry import trace
# from opentelemetry import metrics
# from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
# from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
# from opentelemetry.sdk.resources import SERVICE_NAME, Resource
# from opentelemetry.instrumentation.flask import FlaskInstrumentor


# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


# # # Service name is required for most backends
# # resource = Resource(attributes={
# #     SERVICE_NAME: "nino-flask"
# # })


# # # Matrix
# # reader = PeriodicExportingMetricReader(
# #     OTLPMetricExporter(endpoint="http://otelcol:4317")
# # )
# # meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
# # metrics.set_meter_provider(meter_provider)

# # tracer = trace.get_tracer("diceroller.tracer")
# # # Acquire a meter.
# # meter = metrics.get_meter("diceroller.meter")

# # # Now create a counter instrument to make measurements with
# # roll_counter = meter.create_counter(
# #     "roll_counter",
# #     description="The number of rolls by roll value",
# # )


# # # Trace
# # trace_provider = TracerProvider(resource=resource)
# # processor = BatchSpanProcessor(
# #     ConsoleSpanExporter()
# # )
# # trace_provider.add_span_processor(processor)
# # trace.set_tracer_provider(trace_provider)

# tracer = trace.get_tracer("diceroller.tracer")
# # Acquire a meter.
# meter = metrics.get_meter("diceroller.meter")

# # Now create a counter instrument to make measurements with
# roll_counter = meter.create_counter(
#     "roll_counter",
#     description="The number of rolls by roll value",
# )


# app = Flask(__name__)
# # FlaskInstrumentor().instrument_app(app)

# @app.route("/")
# def hello_world():
#     with tracer.start_as_current_span("do_roll") as rollspan:
#         res = randint(1, 6)
#         rollspan.set_attribute("roll.value", res)
#         # This adds 1 to the counter for the given roll value
#         roll_counter.add(1, {"roll.value": res})
#         return str(res)


