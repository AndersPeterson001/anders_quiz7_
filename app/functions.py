import sqlite3

def init_db():
    """Initializes the database and creates the tasks table if it doesn't exist."""
    with sqlite3.connect('todo_list.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL
            )
        ''')

def add_task(task):
    """Adds a new task to the database."""
    with sqlite3.connect('todo_list.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))

def view_tasks():
    """Returns a list of all tasks from the database."""
    with sqlite3.connect('todo_list.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, task FROM tasks')
        return cursor.fetchall()

def update_task(task_id, new_task):
    """Updates a task in the database."""
    with sqlite3.connect('todo_list.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task, task_id))

def delete_task(task_id):
    """Deletes a task from the database."""
    with sqlite3.connect('todo_list.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

# Example usage
if __name__ == '__main__':
    # Initialize the database
    init_db()

    # Add tasks
    add_task("Learn Python")
    add_task("Go shopping")

    # View tasks
    print("Tasks:", view_tasks())

    # Update a task (assuming task with ID 1 exists)
    update_task(1, "Learn Python Advanced")

    # Delete a task (assuming task with ID 2 exists)
    delete_task(2)

    # View tasks again to see the changes
    print("Updated Tasks:", view_tasks())
