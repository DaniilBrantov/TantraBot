import sqlite3

db = sqlite3.connect('baza.db', check_same_thread=False)
sql = db.cursor()

def initialize_database():
    sql.execute("""CREATE TABLE IF NOT EXISTS users (id BIGINT, nick TEXT, balance INT, access INT, bought INT)""")
    sql.execute("""CREATE TABLE IF NOT EXISTS shop (id INT, name TEXT, price INT, image BLOB, description TEXT, whobuy TEXT)""")


    db.commit()


