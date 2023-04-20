import mysql.connector

def conn():
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SQLplateforme$98"
    )
    return conn

