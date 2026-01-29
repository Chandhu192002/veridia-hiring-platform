import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="veridia_hiring"
    )
    