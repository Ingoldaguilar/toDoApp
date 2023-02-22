# imports
import sqlite3
from tkinter import *

# ---------------- Functions ----------------
# create db
def create_db():
    # create connection
    connection = sqlite3.connect("toDo.db")
    # create cursor
    cursor = connection.cursor()

    try:
        cursor.execute("""
        CREATE TABLE tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name VARCHAR(100) UNIQUE NOT NULL,
                description VARCHAR(1000) NOT NULL
        ) 
        """)
    except sqlite3.OperationalError:
        print("The table 'tasks' already exist.")
    else:
        print("Table 'tasks' created successfully.")

    try:
        # possible changes -> task_id
        cursor.execute("""
        CREATE TABLE users(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name VARCHAR(100) UNIQUE NOT NULL, 
                task_id INTEGER NOT NULL, 
                FOREIGN KEY(task_id) REFERENCES tasks(id)
        ) 
        """)
    except sqlite3.OperationalError:
        print("The table 'users' already exist.")
    else:
        print("Table 'users' created successfully.")

    # close the connection
    connection.close()

# add category
def add_task():
    task_name = input("Name of the new task\n>")
    description = input(f"Insert a description for the task {task_name}\n>")

    connection = sqlite3.connect("toDo.db")
    cursor = connection.cursor()

    try:
        # insert the new category
        cursor.execute(f"INSERT INTO tasks VALUES(null, '{task_name}', '{description}') ")
    except sqlite3.IntegrityError:
        print(f"Error: The task '{task_name}' already exist.")
    else:
        print(f"Task '{task_name}' created successfully.")

    # save and close
    connection.commit()
    connection.close()

# add dish
def add_user():
    connection = sqlite3.connect("toDo.db")
    cursor = connection.cursor()

    # get the dish
    user = input("Name of the new user\n>")
    try:
        cursor.execute(f"INSERT INTO users VALUES(null, '{user}', {user_id}) ")
    except sqlite3.IntegrityError:
        print(f"Error: The user '{user}' already exist.")
    else:
        print(f"User '{user}' created successfully.")

    # save and close
    connection.commit()
    connection.close()
# ---------------- End Functions ----------------

# ---------------- Console ----------------
# create db
# create_db() Don't create the database yet