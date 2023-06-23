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

from . import app

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


FlaskInstrumentor().instrument_app(app)

# Mongo
# NOTE: Need to call instrument before mongoengine initialize.
PymongoInstrumentor().instrument()
db = MongoEngine(app)
class User(db.Document):
    username = db.StringField(required=True)


@app.route('/user', methods={'POST'}, endpoint='create_user')
def create_user():
    payload = request.get_json()

    if not (username := payload.get('username')):
        return Response(status=400)
    
    if user := User.objects.create(username=username):
        response = make_response({
            'id': str(user.id),
            'username': user.username
        })
        response.status = 201
        return response
    

@app.route('/user/<string:user_id>', methods={'GET'}, endpoint='get_user_by_id')
def get_user_by_id(user_id: str):
    
    if not (user := User.objects.filter(id=user_id).first()):
        return Response(status=404)
    

    response = make_response({
        'id': str(user.id),
        'username': user.username
    })
    return response


@app.route("/roll")
def toll_dice2():
    return str(randint(1, 6))

@app.route("/roll-long")
def roll_dice():
    counter.add(1)
    rolled = randint(1, 6)
    time.sleep(0.1 * rolled)
    return str(rolled)
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
