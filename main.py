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

def delete_category():

    connection = sqlite3.connect("toDo.db")
    cursor = connection.cursor()

    # show categories to the user
    categories = cursor.execute("SELECT * FROM categories").fetchall()

    print("\t||Categories||")
    for category in categories:
        print(f">{category[1]}") # name

    cat_name = input("Insert the name of the category you want to delete\n>")

    # Reminder: capture the error when delete a non-existing table
    try:
        # insert the new task
        cursor.execute(f"DELETE FROM categories WHERE name='{cat_name}'")
    except sqlite3.OperationalError:
        print(f"Error: The category  '{cat_name}' doesn't exist.")
    else:
        print(f"Category '{cat_name}' deleted successfully.")

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


def upload_task():

    connection = sqlite3.connect("toDo.db")
    cursor = connection.cursor()

    # show tasks to the user
    tasks = cursor.execute("SELECT * FROM tasks").fetchall()
    print("\t||Tasks||")
    for task in tasks:
        print(f">{task[1]}") # name

    task_name = input("Insert the name of the task you want to upload\n>")
    task_description = cursor.execute(f"SELECT description FROM tasks WHERE name='{task_name}'").fetchone()
    task_category_id = cursor.execute(f"SELECT category_id FROM tasks WHERE name='{task_name}'").fetchone()

    # get if the name exist or not
    exist = False
    for task in tasks:
        if task_name == task[1]:
            exist = True

    if exist:
        # name do exist

        # ---- Name ----
        opc = input("Do you want to upload the name of your task?\n[1] yes\n[2] no\n>")
        if opc == 1:
            # get the new task name
            new_name = input(f"Introduce the new name for the task {task_name}")
        else:
            new_name = task_name

        # ---- Description ----
        opc2 = input("Do you want to upload the description of your task?\n[1] yes\n[2] no\n>")
        if opc2 == 1:
            # get the new task name
            new_description = input(f"Introduce the new description for the task {task_name}")
        else:
            new_description = task_description

        # ---- Category ID ----
        opc3 = input("Do you want to upload the category of your task?\n[1] yes\n[2] no\n>")
        if opc3 == 1:
            # get the new task name
            new_category_id = input(f"Introduce the new category of the task {task_name}")
        else:
            new_category_id = task_category_id

        # ---- Look if he changes something ----
        if opc == 1 or opc2 == 1 or opc3 == 1:
            # if changed something, then try the update
            try:
                cursor.execute(f"UPDATE tasks SET name='{new_name}', description={new_description}, category_id='{new_category_id}' WHERE name='{task_name}'")
            except sqlite3.OperationalError:
                print(f"Error: The task '{task_name}' doesn't exist.")
            else:
                print(f"Task '{task_name}' uploaded successfully.")
        else:
            # if not don't execute it
            print(f"The task '{task_name}' has not been modified.")
    else:
        # name searched doesn't exist
        print(f"Error: The task '{task_name}' doesn't exist.")

    # save and close
    connection.commit()
    connection.close()

def upload_category():

    connection = sqlite3.connect("toDo.db")
    cursor = connection.cursor()

    # show categories to the user
    categories = cursor.execute("SELECT * FROM categories").fetchall()
    print("\t||Categories||")
    for category in categories:
        print(f">{category[1]}") # name

    # --- Get name ---
    cat_name = input("Insert the name of the category you want to delete\n>")

    # ---- verify if the name exists ----
    exist = False
    for cat in categories:
        if cat_name == cat[1]:
            exist = True

    if exist:
        # ---- Name ----
        opc = input("Do you want to upload the name of your category?\n[1] yes\n[2] no\n>")
        if opc == 1:
            # get the new task name
            new_name = input(f"Introduce the new name for the category {cat_name}")

            # upload name
            try:
                cursor.execute(
                    f"UPDATE categories SET name='{new_name}' WHERE name='{cat_name}'")
            except sqlite3.OperationalError:
                print(f"Error: The category '{cat_name}' doesn't exist.")
            else:
                print(f"Category '{cat_name}' uploaded successfully.")
        else:
            print(f"The category '{cat_name}' has not been modified.")
    else:
        print(f"Error: The category '{cat_name}' doesn't exist.")

   # save and close
    connection.commit()
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

"""
Reminder: Some bugs appear, fix them.

> Numbers when showing the tasks or categories.
> The Delete functions, capture the correct error. | Upload: It's no possible to capture that error!

Add an Upload option for both tasks and categories.

Add GUI.
"""

# show menu
while True:
    print("\nWelcome to the To Do App")
    option = input("\nInsert a option:\n[1] Add a category\n[2] Upload a category\n[3] Delete a category\n[4] Add a task\n[5] Upload a task\n[6] Delete a task\n[7] Show tasks\n[8] Exit\n>")

    if option == "1":
        add_category()

    elif option == "3":
        upload_category()

    elif option == "3":
        delete_category()

    elif option == "4":
        add_task()

    elif option == "5":
        upload_task()

    elif option == "6":
        delete_task()

    elif option == "7":
        show_tasks()

    elif option == "8":
        print("Bye!")
        break

    else:
        print("Error: select a valid option")
# ---------------- End Console ----------------