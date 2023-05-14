import os
import sentry_sdk
import sentry_sdk.integrations.flask

from flask import Flask, request, current_app

sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    traces_sample_rate=1.0,
    integrations=[
        sentry_sdk.integrations.flask.FlaskIntegration(),
    ],
)


app = Flask(__name__)

@app.route("/", methods={'POST'})
def hello_world():
    print('before', request.get_json())
    current_app.logger.error('debug example')
    print('after', request.get_json())
    return "<p>Hello, World!</p>"
