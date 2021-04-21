import discord
import sqlite3
from sqlite3 import Error

class sqliteLeaderboard():

    # Try to Establish Database Connection to the SQLite Database
    try:
        conn = sqlite3.connect("leaderboard.db")
        print(sqlite3.version)
    except Error as e:
        print(e)

    # Create a Cursor Object from the Connection
    cursor = conn.cursor()

    # Variables for Creating the Table for Users on the Leaderboard
    sql_create_user_table = ''' CREATE TABLE IF NOT EXISTS users(
        USER_ID INTEGER UNIQUE,
        USER_NAME TEXT NOT NULL,
        WINS INTEGER,
        LOSSES INTEGER
    )'''

    # Create the Table if it doesn't Exist
    cursor.execute(sql_create_user_table)

    '''
    # Create the Database Connection to the SQLite Database
    def create_connection():

        # Instantiate Connection as None
        conn = None

        # Try to Connect the Connection to the SQLite Database
        try:
            conn = sqlite3.connect("leaderboard.db")
            print(sqlite3.version)
        except Error as e:
            print(e)
        
        # Return the Connection
        return conn

    # Function to Create a Table in the SQLite Database
    def create_table(conn, create_table_sql):

        # Try to Create the Table using the Connection
        try:
            c = conn.cursor()
            c.execute(create_table_sql
        except Error as e:
            print(e)

        return
    '''