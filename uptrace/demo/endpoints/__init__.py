import random

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
def roll():
    return str(random.randint(1, 6))
