
import time
import werkzeug
import datetime
import json

from flask import Flask, request, current_app, wrappers

def to_int(value, default=None):
    if isinstance(value, datetime.timedelta):
        value = value.total_seconds()

    try:
        return int(float(value))
    except (ValueError, TypeError):
        pass
    return default


class CacheControlResponseMixin:
    cache_control_class = werkzeug.datastructures.ResponseCacheControl

    @property
    def cache_control(self) -> werkzeug.datastructures.ResponseCacheControl:
        # REF: https://github.com/pallets/werkzeug/blob/2.1.2/src/werkzeug/sansio/response.py#L484
        def on_update(cache_control: werkzeug.datastructures.ResponseCacheControl) -> None:
            if not cache_control and "cache-control" in self.headers:
                del self.headers["cache-control"]
            elif cache_control:
                # NOTE: Private takes precedence over public
                if cache_control.public and cache_control.private:
                    cache_control.public = False

                self.headers["Cache-Control"] = cache_control.to_header()

        return werkzeug.http.parse_cache_control_header(
            self.headers.get("cache-control"), on_update, self.cache_control_class,
        )


class ResponseCacheControl(werkzeug.datastructures.ResponseCacheControl):
    private = werkzeug.datastructures.cache_control.cache_control_property(
        'private', None, bool,
    )
    stale_while_revalidate = werkzeug.datastructures.cache_control.cache_control_property(
        'stale-while-revalidate', None, to_int,
    )
    max_age = werkzeug.datastructures.cache_control.cache_control_property('max-age', -1, to_int)
    s_maxage = werkzeug.datastructures.cache_control.cache_control_property('s-maxage', None, to_int)


class Response(
    CacheControlResponseMixin,
    wrappers.Response,
):
    cache_control_class = ResponseCacheControl


class Flask(Flask):
    response_class = Response

    def make_response(self, *args, status=None, content_type: str=None, mimetype: str=None):
        """
        Custom response serialization for specific types

        flask.make_response only supports positional args
        """
        if not args:
            return self.response_class(
                status=status, content_type=content_type, mimetype=mimetype,
            )

        response, *_ = args

        response_type = type(response)

        if response_type in {dict, list}:
            response = self.response_class(
                json.dumps(response),
                content_type=content_type,
                mimetype='application/json',
                status=status,
            )

            return response

        response = super().make_response(*args)
        if status:
            response.status = status
        if content_type:
            response.content_type = content_type
        if mimetype:
            response.mimetype = mimetype
        return response


app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'


@app.route('/now')
def now():
    now = time.time()
    response = current_app.make_response({'ts': now})
    response.cache_control.public = True
    response.cache_control.max_age = 60
    response.cache_control.s_maxage = 10
    response.cache_control.stale_while_revalidate = 30
    return response


@app.route('/now-private')
def now_private():
    now = time.time()
    response = current_app.make_response({'ts': now})
    response.cache_control.private = True
    response.cache_control.stale_while_revalidate = 30
    return response


@app.route('/now-v2')
def now_v2():
    now = time.time()
    response = current_app.make_response({'ts': now})
    
    public = bool(request.args.get('public'))
    private = bool(request.args.get('private'))

    swr = (swr := request.args.get('swr')) and int(swr)
    max_age = (max_age := request.args.get('max_age')) and int(max_age)
    s_maxage = (s_maxage := request.args.get('s_maxage')) and int(s_maxage)

    if public:
        response.cache_control.public = True

    if private:
        response.cache_control.private = True

    if swr:
        response.cache_control.stale_while_revalidate = swr

    if max_age:
        response.cache_control.max_age = max_age

    if s_maxage:
        response.cache_control.s_maxage = s_maxage    

    return response
