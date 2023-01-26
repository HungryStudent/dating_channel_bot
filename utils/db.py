import sqlite3
from contextlib import closing
from sqlite3 import Cursor

database = "utils/database.db"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def start():
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users(user_id INT, username TEXT, first_name TEXT)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS profiles(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, name TEXT, age INT,"
            "country TEXT, city TEXT, height INT, weight INT, my_size INT, is_move BOOL, description TEXT, gender TEXT)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS photos(profile_id INT, file_id INT)")

        connection.commit()


def get_user(user_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()


def add_user(user_id, username, first_name):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, username, first_name))
        connection.commit()


def create_profile(user_id, profile_data):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("INSERT INTO profiles(user_id, name, age,"
                       "country, city, height, weight, my_size, is_move, description, gender) VALUES (?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?)",
                       (user_id, profile_data["name"], profile_data["age"],
                        profile_data["country"], profile_data["city"], profile_data["height"], profile_data["weight"],
                        profile_data["my_size"], profile_data["is_move"], profile_data["description"],
                        profile_data["gender"]))
        profile_id = cursor.lastrowid
        for photo in profile_data["photos"]:
            cursor.execute("INSERT INTO photos VALUES (?, ?)", (profile_id, photo))
        connection.commit()
        return profile_id


def get_profile(profile_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute(
            "SELECT *, users.username FROM profiles JOIN users on users.user_id = profiles.user_id WHERE id = ?",
            (profile_id,))
        profile_data = cursor.fetchone()
        cursor.execute("SELECT file_id FROM photos WHERE profile_id = ?", (profile_id,))
        photos = [photo["file_id"] for photo in cursor.fetchall()]
        profile_data["photos"] = photos
        return profile_data


def change_param(change_data, value):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute(f"UPDATE profiles SET {change_data['param']} = ? WHERE id = ?",
                       (value, change_data['profile_id']))
        connection.commit()
