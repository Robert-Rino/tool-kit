from flask import Flask
from celery import Celery, Task, signals
from flask_mongoengine import MongoEngine
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor


db = MongoEngine()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('demo.settings.Config')
    app.config.from_prefixed_env()
    celery_init_app(app)
    db.init_app(app)

    from . import endpoints

    app.register_blueprint(endpoints.app)

    return app


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
