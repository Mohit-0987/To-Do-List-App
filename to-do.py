import sqlite3
import os
from flask import Flask, request, jsonify, render_template

# --- App & Database Configuration ---

app = Flask(__name__)

# Define the path for the database. On Render, this will be in the persistent disk.
DATABASE = 'todo.db'

def get_db_connection():
    """Establishes a connection to the database and returns the connection object."""
    conn = sqlite3.connect(DATABASE)
    # This setting allows you to access columns by name, which is more readable.
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Creates the database table if it doesn't already exist."""
    # This function is called once when the application starts.
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# --- Web Page Route ---

@app.route('/')
def home():
    """Serves the main HTML page."""
    return render_template('index.html')

# --- API Routes ---

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    """Endpoint to retrieve all tasks from the database."""
    conn = get_db_connection()
    try:
        tasks_rows = conn.execute('SELECT id, text, completed FROM tasks ORDER BY id').fetchall()
        # Convert the list of database rows into a list of dictionaries
        tasks = [dict(row) for row in tasks_rows]
        return jsonify(tasks)
    finally:
        # Ensure the connection is closed even if an error occurs.
        conn.close()

@app.route('/add_task', methods=['POST'])
def add_new_task():
    """Endpoint to add a new task."""
    data = request.get_json()
    if not data or not data.get('text', '').strip():
        return jsonify({"error": "Task text is required"}), 400

    text = data['text']
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (text, completed) VALUES (?, ?)', (text, 0))
        new_id = cursor.lastrowid
        conn.commit()
        # Return the newly created task to the frontend
        return jsonify({"id": new_id, "text": text, "completed": False}), 201
    finally:
        conn.close()

@app.route('/update_task/<int:task_id>', methods=['PUT'])
def update_existing_task(task_id):
    """Endpoint to mark a task as complete or incomplete."""
    data = request.get_json()
    if 'completed' not in data:
        return jsonify({"error": "Completion status is required"}), 400

    # Convert boolean (true/false) to integer (1/0) for SQLite
    completed_status = 1 if data['completed'] else 0
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (completed_status, task_id))
        conn.commit()

        if cursor.rowcount == 0:
            # This means no task with the given ID was found
            return jsonify({"error": "Task not found"}), 404

        # Fetch the updated task to confirm the change
        updated_task_row = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        return jsonify(dict(updated_task_row))
    finally:
        conn.close()

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_existing_task(task_id):
    """Endpoint to delete a task."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404
        
        return jsonify({"success": "Task deleted"})
    finally:
        conn.close()


# --- Main Execution Block ---

if __name__ == '__main__':
    # When running locally, first ensure the database and table exist.
    create_tables()
    app.run(debug=True, port=5000)
else:
    # When running in production (like on Render), also ensure the DB exists.
    create_tables()
