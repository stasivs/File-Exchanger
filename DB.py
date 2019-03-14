import sqlite3
from Tools import *
from flask import render_template, make_response, request, redirect
from flask import session
from flask_restful import Resource, abort


class DB:
    def __init__(self, name):
        conn = sqlite3.connect(name, check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UserModel:
    def __init__(self, connection):
        self.connection = connection
        self.init_table()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash) 
                          VALUES (?,?)''', (user_name, password_hash))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def delete(self, arch_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM archives WHERE id = ?''', (str(arch_id),))
        cursor.close()
        self.connection.commit()

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)


class Archives:
    def __init__(self, connection):
        self.connection = connection
        self.init_table()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS archives 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             url VARCHAR(25),
                             user_name VARCHAR(100)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, url, user_name=None,):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO archives 
                          (user_name, url) 
                          VALUES (?,?)''', (str(user_name), url))
        cursor.close()
        self.connection.commit()

    def get(self, arch_url):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM archives WHERE url = ?", (arch_url,))
        row = cursor.fetchone()
        return row

    def get_all(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM archives WHERE user_name = ?",
                       (str(user_name),))
        rows = cursor.fetchall()
        return rows

    def delete(self, arch_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM archives WHERE id = ?''', (str(arch_id),))
        cursor.close()
        self.connection.commit()


def abort_if_arch_not_found(url):
    if not Archives(db.get_connection()).get(url):
        abort(404, message="Hello!")


class Archive(Resource):
    def get(self, url):
        abort_if_arch_not_found(url)
        return make_response(render_template("Download_template.html", url=url + ".txt"))

    def delete(self, arch_id):
        Archives(db.get_connection()).delete(arch_id)


class MakeArchive(Resource):
    def get(self):
        return make_response(render_template("Make_Archive.html"))

    def post(self):
        f = request.files['file'].read()
        url = str(create_url())
        with open("Archives/" + url + ".txt", "wb") as file:
            file.write(f)
        if 'username' in session:
            Archives(db.get_connection()).insert(url, session['username'])
        else:
            Archives(db.get_connection()).insert(url)
        return make_response(render_template("url.html", url=url))


class Login(Resource):
    def get(self):
        form = LoginForm()
        return make_response(render_template("Login.html", form=form))

    def post(self):
        form = LoginForm()
        username = form.username.data
        password = form.password.data
        temp = UserModel(db.get_connection()).get(username)
        print(temp)
        if temp:
            session['username'] = username
            return make_response(render_template("Make_Archive.html"))
        else:
            return "B"


class Registration(Resource):
    def get(self):
        form = LoginForm()
        return make_response(render_template("Registration.html", form=form))

    def post(self):
        form = LoginForm()
        username = form.username.data
        password = form.password.data
        UserModel(db.get_connection()).insert(username, password)
        return redirect("/")


class Logout(Resource):
    def get(self):
        session.pop('username', 0)
        return redirect("/")


class MyArchives(Resource):
    def get(self, username):
        if 'username' in session and session['username'] == username.strip():
            archive_list = Archives(db.get_connection()).get_all(username.strip())
            return make_response(render_template("User_Archives.html",
                                                 archive_list=archive_list))
        else:
            return redirect("/")


db = DB("DB.db")
