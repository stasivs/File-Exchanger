import os

from Tools import *
from flask import render_template, make_response, request, redirect
from flask import session
from flask_restful import Resource, abort


def abort_if_arch_not_found(url):
    if not Archives(db.get_connection()).get(url):
        return abort(404, message="Not found")


class Archive(Resource):
    def get(self, url):
        abort_if_arch_not_found(url)
        arch = Archives(db.get_connection()).get(url)
        return make_response(render_template("Download_template.html",
                                             title=arch[1], info=arch[2], username=arch[5], url=(arch[3] + arch[4])))

    def delete(self, arch_id):
        Archives(db.get_connection()).delete(arch_id)


class MakeArchive(Resource):
    def get(self):
        form = AddArchive()
        return make_response(render_template("Make_Archive.html", form=form))

    def post(self):
        form = AddArchive()
        title = form.title.data
        info = form.info.data
        file = form.file.data.read()
        url = str(create_url())
        format = "." + form.file.data.filename.split(".")[-1]
        with open("static/" + url + format, "wb") as f:
            f.write(file)
        if 'username' in session:
            Archives(db.get_connection()).insert(title, info, url, format, session['username'])
        else:
            Archives(db.get_connection()).insert(title, info, url, format)
        return make_response(render_template("url.html", url=url))


class Login(Resource):
    def get(self):
        form = LoginForm()
        return make_response(render_template("Login.html", form=form))

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            temp = UserModel(db.get_connection()).get(username)
            if temp:
                password_encrypt = hashlib.md5(bytes(password, "utf-8"))
                password_encrypt = password_encrypt.hexdigest()
                if temp[-1] == password_encrypt:
                    session['username'] = username.strip()
                    return redirect("/")
                else:
                    return "S"
        else:
            return make_response(render_template('login.html', form=form))


class Registration(Resource):
    def get(self):
        form = RegistrationForm()
        return make_response(render_template("Registration.html", form=form))

    def post(self):
        form = RegistrationForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            password_encrypt = hashlib.md5(bytes(password, "utf-8"))
            password_encrypt = password_encrypt.hexdigest()
            UserModel(db.get_connection()).insert(username, password_encrypt)
            return redirect("/")
        return make_response(render_template('Registration.html', form=form))


class Logout(Resource):
    def get(self):
        session.pop('username', 0)
        return redirect("/")


class MyArchives(Resource):
    def get(self, username):
        username = username.strip()
        if 'username' in session and session['username'] == username:
            archive_list = Archives(db.get_connection()).get_all(username)
            return make_response(render_template("User_Archives.html",
                                                 archive_list=archive_list))
        else:
            return redirect("/")
