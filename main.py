import tkinter as tk
from tkinter import simpledialog
import sqlite3

def init_db():
    """Initializes the SQLite database and creates a 'tasks' table if it does not already exist."""
    with sqlite3.connect('todo_list.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL
            )
        ''')

def add_task(task):
    """Adds a new task to the database and refreshes the task list in the GUI."""
    with sqlite3.connect('todo_list.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    refresh_tasks()

def view_tasks():
    """Fetches and returns all tasks from the database."""
    with sqlite3.connect('todo_list.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, task FROM tasks')
        return cursor.fetchall()

def update_task(task_id, new_task):
    """Updates the content of a task based on its ID."""
    with sqlite3.connect('todo_list.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task, task_id))
    refresh_tasks()

def delete_task(task_id):
    """Deletes a task from the database based on its ID."""
    with sqlite3.connect('todo_list.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    refresh_tasks()

def refresh_tasks():
    """Refreshes the task list in the GUI to reflect the current state of the database."""
    listbox_tasks.delete(0, tk.END)
    for task_id, task in view_tasks():
        listbox_tasks.insert(tk.END, (task_id, task))

def edit_task_popup():
    """Handles the logic for editing a task through a popup dialog."""
    try:
        task_id, task_content = listbox_tasks.get(listbox_tasks.curselection())
    except IndexError:
        # Nothing selected; do nothing
        return
    new_task = simpledialog.askstring("Edit Task", "Edit your task:", initialvalue=task_content)
    if new_task:
        update_task(task_id, new_task)

def main():
    """Main function setting up the Tkinter GUI."""
    global listbox_tasks
    init_db()

    root = tk.Tk()
    root.title("Anders Peterson To-Do List")
    root.geometry("600x600")

    tk.Label(root, text="Enter a Task:").pack()
    entry_task = tk.Entry(root)
    entry_task.pack()

    tk.Button(root, text="Add", command=lambda: add_task(entry_task.get())).pack()

    listbox_tasks = tk.Listbox(root)
    listbox_tasks.pack()
    listbox_tasks.bind('<Double-1>', lambda event: edit_task_popup())

    tk.Button(root, text="Delete Selected", command=lambda: delete_task(listbox_tasks.get(listbox_tasks.curselection())[0])).pack()

    refresh_tasks()

    root.mainloop()

if __name__ == "__main__":
    main()
