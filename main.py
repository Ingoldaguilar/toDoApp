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
        # possible changes -> task_id
        cursor.execute("""
        CREATE TABLE categories(
                cat_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name VARCHAR(100) UNIQUE NOT NULL
        ) 
        """)
    except sqlite3.OperationalError:
        print("The table 'categories' already exist.")
    else:
        print("Table 'categories' created successfully.")

    try:
        cursor.execute("""
        CREATE TABLE tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name VARCHAR(100) UNIQUE NOT NULL,
                description VARCHAR(1000) NOT NULL,
                FOREIGN KEY(id) REFERENCES categories(cat_id)
        ) 
        """)
    except sqlite3.OperationalError:
        print("The table 'tasks' already exist.")
    else:
        print("Table 'tasks' created successfully.")

    # close the connection
    connection.close()

# add category
def add_category():
    category = input("Name of the new category\n>")

    connection = sqlite3.connect("toDo.db")
    cursor = connection.cursor()

    try:
        # insert the new category
        cursor.execute(f"INSERT INTO categories VALUES(null, '{category}') ")
    except sqlite3.IntegrityError:
        print(f"Error: The category '{category}' already exist.")
    else:
        print(f"Category '{category}' created successfully.")

    # save and close
    connection.commit()
    connection.close()

# add task
def add_task():
    task_name = input("Name of the new task\n>")
    description = input(f"Insert a description for the task {task_name}\n>")

    connection = sqlite3.connect("toDo.db")
    cursor = connection.cursor()

    try:
        # insert the new task
        cursor.execute(f"INSERT INTO tasks VALUES(null, '{task_name}', '{description}') ")
    except sqlite3.IntegrityError:
        print(f"Error: The task '{task_name}' already exist.")
    else:
        print(f"Task '{task_name}' created successfully.")

    # save and close
    connection.commit()
    connection.close()
# ---------------- End Functions ----------------

# ---------------- Console ----------------
# create db
# create_db() Don't create the database yet