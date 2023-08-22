import sqlite3
from utils import utils


class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def create_db(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY NOT NULL,
            user_id INTEGER NOT NULL,
            username TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY NOT NULL,
            who_user INTEGER NOT NULL,
            title TEXT,
            desc TEXT,
            file_id TEXT,
            task_date TEXT
        )
        ''')

        self.conn.commit()

    def add_user(self, user_id, username):
        try:
            self.cursor.execute('INSERT INTO users (user_id, username) VALUES (?,?);',
                                (user_id, username))
            self.conn.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def get_user_by_user_id(self, user_id):
        try:
            self.cursor.execute('SELECT * FROM users WHERE user_id=?;', (user_id,))
            return self.cursor.fetchone()
        except Exception as ex:
            print(ex)
            return False

    def get_user_by_username(self, username):
        try:
            self.cursor.execute('SELECT * FROM users WHERE username=?;', (username,))
            return self.cursor.fetchone()
        except Exception as ex:
            print(ex)
            return False

    def get_users(self):
        self.cursor.execute('SELECT user_id FROM users')
        spam_base = self.cursor.fetchall()
        return spam_base

    def add_task(self, who_user, title, desc, file_id):
        task_date = utils.get_now_date()
        try:
            self.cursor.execute('INSERT INTO tasks (who_user, title, desc, task_date, file_id) VALUES (?,?,?,?,?);',
                                (who_user, title, desc, task_date, file_id))
            self.conn.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def update_task_title(self, who_user, new_title, task_id):
        try:
            self.cursor.execute('UPDATE tasks SET title=? WHERE who_user=? AND id=?;',
                                (new_title, who_user, task_id))
            self.conn.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def update_task_desc(self, who_user, new_desc, task_id):
        try:
            self.cursor.execute('UPDATE tasks SET desc=? WHERE who_user=? AND id=?;',
                                (new_desc, who_user, task_id))
            self.conn.commit()
        except Exception as ex:
            print(ex)
            return False

    def update_task_date(self, who_user, new_date, task_id):
        try:
            self.cursor.execute('UPDATE tasks SET task_date=? WHERE who_user=? AND id=?;',
                                (new_date, who_user, task_id))
            self.conn.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def update_task_url(self, who_user, new_file_id, task_id):
        try:
            self.cursor.execute('UPDATE tasks SET file_id=? WHERE who_user=? AND id=?;',
                                (new_file_id, who_user, task_id))
            self.conn.commit()
        except Exception as ex:
            print(ex)
            return False

    def get_user_tasks(self, who_user):
        try:
            self.cursor.execute('SELECT * FROM tasks WHERE who_user=?;', (who_user,))
            return self.cursor.fetchall()
        except Exception as ex:
            print(ex)
            return False

    def get_user_task_by_title(self, who_user, task_title):
        try:
            self.cursor.execute('SELECT * FROM tasks WHERE who_user=? AND title=?;',
                                (who_user, task_title))
        except Exception as ex:
            print(ex)
            return False

    def get_user_task_by_id(self, who_user, task_id):
        try:
            self.cursor.execute('SELECT * FROM tasks WHERE who_user=? AND id=?;',
                                (who_user, task_id))
            return self.cursor.fetchone()
        except Exception as ex:
            print(ex)
            return False

    def delete_task(self, task_id, who_user):
        try:
            self.cursor.execute('DELETE FROM tasks WHERE id=? AND who_user=?;',
                                (task_id, who_user))
            self.conn.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def delete_tasks(self, who_user):
        try:
            self.cursor.execute('DELETE FROM tasks WHERE who_user=?;',
                                (who_user,))
            self.conn.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def delete_all_tasks(self):
        try:
            self.cursor.execute('DELETE * from tasks')
            self.conn.commit()
            return True
        except Exception as ex:
            print(ex)
            return False
