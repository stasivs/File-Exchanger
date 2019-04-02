import os

from Tools import *
from flask import render_template, make_response, request, redirect
from flask import session
from flask_restful import Resource, abort


def abort_if_arch_not_found(url):
    if not Files(db.get_connection()).get(url):
        return abort(404, message="Not found")


class File(Resource):
    def get(self, url):
        abort_if_arch_not_found(url)
        arch = Files(db.get_connection()).get(url)
        return make_response(render_template("Download_template.html",
                                             title=arch[1], info=arch[2], username=arch[5], url=(arch[3] + arch[4])))

    def delete(self, arch_id):
        Files(db.get_connection()).delete(arch_id)


class MakeFile(Resource):
    def get(self):
        form = AddFile()
        print("Hi")
        return make_response(render_template("Make_Archive.html", form=form))

    def post(self):
        form = AddFile()
        print(form.title.data, form.info.data, form.file.data)
        print(form.validate_on_submit())
        if form.validate_on_submit():
            title = form.title.data
            info = form.info.data
            file = form.file.data.read()
            url = str(create_url())
            format = "." + form.file.data.filename.split(".")[-1]
            with open(os.path.abspath(os.path.join("static/", url + format)), "wb") as f:
                f.write(file)
            if 'username' in session:
                Files(db.get_connection()).insert(title, info, url, format, session['username'])
            else:
                Files(db.get_connection()).insert(title, info, url, format)
            return make_response(render_template("url.html", url=url))
        else:
            return make_response(render_template("Make_Archive.html", form=form))


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


class MyFiles(Resource):
    def get(self, username):
        username = username.strip()
        if 'username' in session and session['username'] == username:
            archive_list = Files(db.get_connection()).get_all(username)
            return make_response(render_template("User_File.html",
                                                 archive_list=archive_list))
        else:
            return redirect("/")


class Folder(Resource):
    def get(self, folder_url):
        row = Folders(db.get_connection()).get(folder_url)
        title = row[1]
        form = AddFile()
        return make_response(render_template("Folder.html", form=form, title=title))

    def post(self, folder_url):
        form = AddFile()
        title = form.title.data
        info = form.info.data
        file = form.file.data.read()
        url = str(create_url())
        format = "." + form.file.data.filename.split(".")[-1]
        with open(os.path.abspath(os.path.join("static/", url + format)), "wb") as f:
            f.write(file)
        Files(db.get_connection()).insert(title, info, url, format, session['username'], folder_url)
        return make_response(render_template("Folder.html", form=form))


class MakeFolder(Resource):
    def get(self):
        if 'username' in session:
            form = AddFolder()
            return make_response(render_template("Make_folder.html", form=form))
        else:
            return redirect("/login")

    def post(self):
        form = AddFolder()
        title = form.title.data
        url = create_url(15)
        Folders(db.get_connection()).insert(title, url, session['username'])
        return redirect("/{}/folder_files".format(url))
