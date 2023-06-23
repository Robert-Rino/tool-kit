import random
import time

from flask import Blueprint, request, make_response, Response

from demo.models import User

from demo import tasks

app = Blueprint( 'endpoints', __name__)


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
    if not (username := tasks.get_username_by_id.delay(
        user_id=user_id
    ).get()):
        return Response(status=404)
    

    response = make_response({
        'id': user_id,
        'username': username,
    })
    return response


@app.route("/roll")
def toll_dice2():
    return str(random.randint(1, 6))

@app.route("/roll-long")
def roll_dice():
    # counter.add(1)
    rolled = random.randint(1, 6)
    time.sleep(0.1 * rolled)
    return str(rolled)
    return str(do_roll())

# def do_roll():
#     with tracer.start_as_current_span("main") as rollspan:
#         trace_id = rollspan.get_span_context().trace_id
#         print(f"trace id: {trace_id:0{32}x}")
#         res = randint(1, 6)
#         rollspan.set_attribute("roll.value", res)
#         # This adds 1 to the counter for the given roll value
#         # roll_counter.add(1, {"roll.value": res})
#         return res
