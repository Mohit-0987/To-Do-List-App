import sqlite3
from flask import Flask, request, jsonify, render_template

# Create a Flask application instance
app = Flask(__name__)


# --- Database Setup ---

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect('todo.db')
    # This allows accessing columns by name (like a dictionary)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database and creates the 'tasks' table if it doesn't exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# --- The in-memory list has been REMOVED ---
# We now use the SQLite database for storage.


## --- HTML Rendering ---

@app.route('/')
def home():
    """Serves the main HTML page from the 'templates' folder."""
    return render_template('index.html')


## --- API Endpoints (Modified for SQLite) ---

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Endpoint to get all tasks from the database."""
    conn = get_db_connection()
    # Fetch all tasks and order them by ID
    tasks_rows = conn.execute('SELECT * FROM tasks ORDER BY id').fetchall()
    conn.close()
    # Convert database rows to a list of dictionaries
    tasks = [dict(row) for row in tasks_rows]
    return jsonify(tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    """Endpoint to add a new task to the database."""
    data = request.get_json()

    if not data or 'text' not in data or not data['text'].strip():
        return jsonify({"error": "Task text is required"}), 400

    text = data['text']
    # 'completed' is stored as an integer (0 for False, 1 for True)
    completed = 0

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (text, completed) VALUES (?, ?)', (text, completed))
    new_id = cursor.lastrowid  # Get the ID of the newly inserted task
    conn.commit()
    conn.close()

    new_task = {"id": new_id, "text": text, "completed": False}
    return jsonify(new_task), 201


@app.route('/update_task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Endpoint to update a task's completion status in the database."""
    data = request.get_json()
    is_completed = data.get('completed')

    # Convert boolean from frontend to integer for SQLite
    completed_int = 1 if is_completed else 0

    conn = get_db_connection()
    # Update the task and check if any row was affected
    cursor = conn.execute('UPDATE tasks SET completed = ? WHERE id = ?', (completed_int, task_id))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    # Fetch the updated task to return it
    updated_task_row = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()

    return jsonify(dict(updated_task_row))


@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Endpoint to delete a task from the database."""
    conn = get_db_connection()
    cursor = conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"success": "Task deleted successfully"})


# --- Main Execution Block ---

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)