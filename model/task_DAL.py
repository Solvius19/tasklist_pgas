import sqlite3

def get_connection():
    conn = sqlite3.connect('database/tasklist.sqlite')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def get_classes():
    rows = None
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT name FROM Class
                           ''')
            rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Failed to get all classes: {e}")
    return [row[0] for row in rows]

def get_tasks_for_class(class_id):
    rows = None
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM Task 
                WHERE class_id = ?
            ''', [class_id])
            rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Failed to get all tasks: {e}")
    return rows


def delete_task(class_id, task_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            DELETE FROM Task
            WHERE Task.task_id = ?
            ''', task_id)
    except sqlite3.OperationalError as e:
        print(f"Failed to remove task: {e}")