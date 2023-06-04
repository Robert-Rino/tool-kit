import os

from flask import Flask, request, current_app


app = Flask(__name__)

@app.route('/', methods={'GET'})
def hello_world():
    print(request.headers)
    ssl_client = request.headers.get('ssl_client')
    SSL_Client_Issuer = request.headers.get('SSL_Client_Issuer')

    print(f'Hello {ssl_client}, your certificate was issued by {SSL_Client_Issuer}!')
    return "<p>Hello, World!</p>"
