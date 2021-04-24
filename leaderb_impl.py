import discord
import sqlite3
from sqlite3 import Error

class sqliteLeaderboard():

    # Function to Create the Database Connection to the SQLite Database
    def create_connection():

        # Instantiate Connection Variable
        conn = None

        # Try to Establish Database Connection to the SQLite Database
        try:
            conn = sqlite3.connect("leaderboard.db")
            print(sqlite3.version)
        except Error as e:
            print(e)

        # Return the Connection
        return conn

    
    # Function to Create a Table in the SQLite Database
    def create_table(conn):

        # Create a Cursor Object from the Connection
        cursor = conn.cursor()

        # Variables for Creating the Table for Users on the Leaderboard
        sql_create_user_table = ''' CREATE TABLE IF NOT EXISTS USERS(
            USER_ID INTEGER UNIQUE,
            USER_NAME TEXT NOT NULL,
            WINS INTEGER,
            LOSSES INTEGER
        )'''

        # Try to Create the Table (if it doesn't Exist) using the Cursor
        try:
            cursor.execute(sql_create_user_table)
        except Error as e:
            print(e)

        return

    # Function to Insert a User into the Users Table
    def insert_user(ctx, conn, userID, userName):

        # Create a Cursor Object from the Connection
        cursor = conn.cursor()

        # Try to Insert the User into the User Table
        try:
            cursor.execute(''' INSERT INTO USERS(USER_ID, USER_NAME, WINS, LOSSES)
                VALUES (f'{userID}', {userName}, 0, 0)
            ''')
        except Error as e:
            print(e)

        # Commit the Changes to the Database
        conn.commit()

        return


    # Function to Update the Leaderboard Wins and Loses
    def update_leaderboard(ctx, conn, winnerID, loserID, winnerName, loserName):

        # Create a Cursor Object from the Connection
        cursor = conn.cursor()

        # Fetching all the Rows of Data before the Update
        print("Contents of the User Table (Before): ")
        cursor.execute('''SELECT * FROM USERS''')
        print(cursor.fetchall())

        # Make the Update
        sql_update_winner = '''UPDATE USERS SET WINS=WINS+1 WHERE USER_ID={winnerID}'''
        cursor.execute(sql_update_winner)
        sql_update_loser = '''UPDATE USERS SET LOSSES=LOSSES+1 WHERE USER_ID={loserID}'''
        cursor.execute(sql_update_loser)
        print("Update Completed")

        # Fetching all the Rows of Data after the Update
        print("Contents of the User Table (After): ")
        cursor.execute('''SELECT * FROM USERS''')
        print(cursor.fetchall())

        # Commit Changes Made to the Database
        conn.commit()

        return


    # Function to Display the Leaderboard
    def display_leaderboard(ctx, conn):

        # Create a Cursor Object from the Connection
        cursor = conn.cursor()

        # Fetching all the Rows of Data and Order by Wins
        cursor.execute('''SELECT * FROM USERS ORDER BY WINS''')
        
        # Display for Testing Purposes
        print(cursor.fetchall())

        return

    # Function to Close the Connection
    def close_connection(ctx, conn):

        # Try to Close the Connection
        try:
            conn.close()
            print("Connection Successfully Closed.")
        except Error as e:
            print(e)

        return