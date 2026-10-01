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


def delete_task(task_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            DELETE FROM Task
                WHERE task_id = ?
                ''', [task_id])
    except sqlite3.OperationalError as e:
        print(f"Failed to remove task: {e}")


def add_task(t_class, t_name, t_date):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO Task (class_id, task_name, due_date)
            VALUES (?, ?, ?)
            ''', (t_class, t_name, t_date))
    except sqlite3.OperationalError as e:
        print(f"Failed to add task: {e}")
    return None


def get_class_id(class_name):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT class_id FROM Class
            WHERE name = ?
            ''', (class_name,))
            row = cursor.fetchone()
            if row:
                return row[0]
    except sqlite3.OperationalError as e:
        print(f"Failed to get class id: {e}")
    return None