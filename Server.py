from flask import Flask, url_for
from flask_restful import reqparse, abort, Api
from DB import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Archive, '/<string:url>')
api.add_resource(MakeArchive, '/')
api.add_resource(Login, "/login")

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

if __name__ == "__main__":
    app.run("127.0.0.1", 8080, debug=True)