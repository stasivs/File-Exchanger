import sqlite3


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
                             user_name VARCHAR(20),
                             encrypted_password VARCHAR(128)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, encrypted_password) 
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
        cursor.execute('''DELETE FROM file WHERE id = ?''', (str(arch_id),))
        cursor.close()
        self.connection.commit()


class Files:
    def __init__(self, connection):
        self.connection = connection
        self.init_table()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS file 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(50),
                             info VARCHAR(1000),
                             url VARCHAR(25),
                             format VARCHAR(20),
                             user_name VARCHAR(20),
                             folder VARCHAR(15)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, info, url, format, user_name=None, folder=None):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO file 
                          (user_name, title, info, url, format, folder) 
                          VALUES (?,?,?,?,?,?)''', (str(user_name), title, info, url, format, folder))
        cursor.close()
        self.connection.commit()

    def get(self, arch_url):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM file WHERE url = ?", (arch_url,))
        row = cursor.fetchone()
        return row

    def get_all_user_solo_files(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM file WHERE user_name = ? AND folder is null",
                       (str(user_name),))
        rows = cursor.fetchall()
        return rows

    def get_all_user_dirs(self, user_name):
        pass

    def folder_files(self, folder_url):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM file WHERE folder = ?", (str(folder_url),))
        rows = cursor.fetchall()
        return rows

    def delete(self, arch_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM file WHERE id = ?''', (str(arch_id),))
        cursor.close()
        self.connection.commit()


class Folders:
    def __init__(self, connection):
        self.connection = connection
        self.init_table()
        
    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS folders 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(50),
                             user_name VARCHAR(20),
                             url VARCHAR(15)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, url, user_name=None):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO folders
                          (user_name, title, url) 
                          VALUES (?,?,?)''', (str(user_name), title, url))
        cursor.close()
        self.connection.commit()

    def get(self, folder_url):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM folders WHERE url = ?", (folder_url,))
        row = cursor.fetchone()
        return row

    def get_all_user_folders(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM folders WHERE user_name = ?",
                       (str(user_name),))
        rows = cursor.fetchall()
        return rows

db = DB("DB.db")
