import os

from tools import *
from flask import render_template, make_response, request, redirect
from flask import session
from flask_restful import Resource, abort
from zipfile import ZipFile


def abort_if_arch_not_found(url):
    if not Files(db.get_connection()).get(url):
        return abort(404, message="Not found")


class File(Resource):
    def get(self, url):
        abort_if_arch_not_found(url)
        arch = Files(db.get_connection()).get(url)
        return make_response(render_template("download_template.html",
                                             title=arch[1], info=arch[2], username=arch[5], url=(arch[3] + arch[4])))

    def delete(self, arch_id):
        Files(db.get_connection()).delete(arch_id)


class MakeFile(Resource):
    def get(self):
        form = AddFile()
        return make_response(render_template("make_archive.html", form=form))

    def post(self):
        form = AddFile()
        if form.validate_on_submit():
            title = form.title.data
            info = form.info.data
            file = form.file.data.read()
            url = str(create_url())
            format = os.path.splitext(form.file.data.filename)[1]
            with open(os.path.abspath(os.path.join("static/", url + format)), "wb") as f:
                f.write(file)
            if 'username' in session:
                Files(db.get_connection()).insert(title, info, url, format, session['username'])
            else:
                Files(db.get_connection()).insert(title, info, url, format)
            return make_response(render_template("url.html", url=url))
        else:
            return make_response(render_template("make_archive.html", form=form))


class Login(Resource):
    def get(self):
        form = LoginForm()
        return make_response(render_template("login.html", form=form))

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
        return make_response(render_template("registration.html", form=form))

    def post(self):
        form = RegistrationForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            password_encrypt = hashlib.md5(bytes(password, "utf-8"))
            password_encrypt = password_encrypt.hexdigest()
            UserModel(db.get_connection()).insert(username, password_encrypt)
            return redirect("/")
        return make_response(render_template('registration.html', form=form))


class Logout(Resource):
    def get(self):
        session.pop('username', 0)
        return redirect("/")


class MyFiles(Resource):
    def get(self, username):
        username = username.strip()
        if 'username' in session and session['username'] == username:
            archive_list = Files(db.get_connection()).get_all_user_solo_files(username)
            folders = Folders(db.get_connection()).get_all_user_folders(username)
            return make_response(render_template("user_file.html",
                                                 archive_list=archive_list, folders=folders))
        else:
            return redirect("/")


class Folder(Resource):
    def get(self, folder_url):
        row = Folders(db.get_connection()).get(folder_url)
        title = row[1]
        username = row[2]
        form = AddFile()
        archive_list = Files(db.get_connection()).folder_files(folder_url)
        return make_response(render_template("folder.html", form=form, title=title, archive_list=archive_list,
                                             url=folder_url + ".zip", username=username))

    def post(self, folder_url):
        form = AddFile()
        if form.validate_on_submit():
            title = form.title.data
            info = form.info.data
            file = form.file.data.read()
            url = str(create_url())
            format = os.path.splitext(form.file.data.filename)[1]
            with open(os.path.abspath(os.path.join("static/", url + format)), "wb") as f:
                f.write(file)
            Files(db.get_connection()).insert(title, info, url, format, session['username'], folder_url)
            with ZipFile(os.path.abspath(os.path.join("static/", "{}.zip".format(folder_url))), "w") as archive:
                for file in Files(db.get_connection()).folder_files(folder_url):
                    archive.write("static/{}{}".format(file[3], file[4]))
        return redirect("/{}/folder_files".format(folder_url))


class MakeFolder(Resource):
    def get(self):
        if 'username' in session:
            form = AddFolder()
            return make_response(render_template("make_folder.html", form=form))
        else:
            return redirect("/login")

    def post(self):
        form = AddFolder()
        title = form.title.data
        url = create_url(15)
        Folders(db.get_connection()).insert(title, url, session['username'])
        return redirect("/{}/folder_files".format(url))
