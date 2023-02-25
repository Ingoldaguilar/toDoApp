# imports
import sqlite3
# from tkinter import *

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
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
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
                category_id INTEGER NOT NULL, 
                FOREIGN KEY(category_id) REFERENCES categories(id)
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

    connection = sqlite3.connect("toDo.db")
    cursor = connection.cursor()

    task_name = input("Name of the new task\n>")
    description = input(f"Insert a description for the task {task_name}\n>")

    # show categories to the user
    categories = cursor.execute("SELECT * FROM categories").fetchall()

    print("Select a category for the task:")
    for category in categories:
        print(f"[{category[0]}] {category[1]}") # id and name

    # get the category
    category_id = int( input(">") )

    try:
        # insert the new task
        cursor.execute(f"INSERT INTO tasks VALUES(null, '{task_name}', '{description}', {category_id}) ")
    except sqlite3.IntegrityError:
        print(f"Error: The task '{task_name}' already exist.")
    else:
        print(f"Task '{task_name}' created successfully.")

    # save and close
    connection.commit()
    connection.close()


def delete_task():

    connection = sqlite3.connect("toDo.db")
    cursor = connection.cursor()

    # show categories to the user
    tasks = cursor.execute("SELECT * FROM tasks").fetchall()

    print("\t||Tasks||")
    for task in tasks:
        print(f">{task[1]}") # name

    task_name = input("Insert the name of the task you want to delete\n>")

    # Reminder: capture the error when delete a non-existing table
    try:
        # insert the new task
        cursor.execute(f"DELETE FROM tasks WHERE name='{task_name}'")
    except sqlite3.OperationalError:
        print(f"Error: The task '{task_name}' doesn't exist.")
    else:
        print(f"Task '{task_name}' deleted successfully.")

    # save and close
    connection.commit()
    connection.close()

# show menu
def show_tasks():

    connection = sqlite3.connect("toDo.db")
    cursor = connection.cursor()

    categories = cursor.execute("SELECT * FROM categories").fetchall()
    for category in categories:
        print("||"+category[1]+"||")
        tasks = cursor.execute(f"SELECT * FROM tasks WHERE id={category[0]}").fetchall()
        for task in tasks:
            print(f"\t>{task[1]}")
            print(f"\t  .{task[2]}")

    # save and close
    connection.close()
# ---------------- End Functions ----------------

# ---------------- GUI ----------------
# root
#root = Tk()
#root.title("To Do App")
#root.iconbitmap("toDoIcon.ico")
#root.resizable(False, False)
#root.geometry("500x500")


 # Buttons
#Button(text="Exit", command=root.quit).pack()

# mainloop
#root.mainloop()
# ---------------- End GUI ----------------

# ---------------- Console ----------------
# create_db() database created.

# show menu
while True:
    print("\nWelcome to the To Do App")
    option = input("\nInsert a option:\n[1] Add a category\n[2] Add a task\n[3] Delete a task\n[4] Show tasks\n[5] Exit\n>")

    if option == "1":
        add_category()

    elif option == "2":
        add_task()

    elif option == "3":
        delete_task()

    elif option == "4":
        show_tasks()

    elif option == "5":
        print("Bye!")
        break

    else:
        print("Error: select a valid option")
# ---------------- End Console ----------------