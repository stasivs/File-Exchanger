from flask import Flask, url_for
from links import *
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

api.add_resource(File, '/<string:url>')
api.add_resource(MakeFile, '/')
api.add_resource(Login, "/login")
api.add_resource(Registration, "/registration")
api.add_resource(Logout, "/logout")
api.add_resource(MyFiles, "/<string:username>/user_files")
api.add_resource(Folder, "/<string:folder_url>/folder_files")
api.add_resource(MakeFolder, "/folder")

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

if __name__ == "__main__":
    app.run("127.0.0.1", 8080, debug=True)
