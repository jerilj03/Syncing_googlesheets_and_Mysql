import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        user='root',
        password='1915',
        database='my_db'
    )