# Import necessary libraries
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from vercel_kv import KV  # <-- FIX 1: Import uppercase 'KV'
import time

# Create a Flask application instance
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# FIX 2: Create an instance of the KV client
kv_store = KV()

# --- Route for the Homepage ---
@app.route('/')
def home():
    """
    This function remains the same. It serves the frontend HTML file.
    """
    return render_template('frontend.html')


# --- API Endpoints Modified for Vercel KV ---

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Endpoint to get all tasks from Vercel KV."""
    # .get() will return None if 'tasks' doesn't exist, so we use 'or []' as a fallback.
    tasks = kv_store.get('tasks') or [] # <-- Use the instance
    return jsonify(tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    """Endpoint to add a new task and save it to Vercel KV."""
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Task text is required"}), 400

    # Retrieve the current list of tasks from KV
    tasks = kv_store.get('tasks') or [] # <-- Use the instance

    # Create the new task. Using a timestamp for the ID ensures uniqueness.
    new_task = {
        "id": int(time.time() * 1000),  # Use milliseconds timestamp for a unique ID
        "text": data['text'],
        "completed": False
    }
    tasks.append(new_task)

    # Save the entire updated list back to Vercel KV
    kv_store.set('tasks', tasks) # <-- Use the instance

    return jsonify(new_task), 201

@app.route('/update_task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Endpoint to update a task's status in Vercel KV."""
    data = request.get_json()
    tasks = kv_store.get('tasks') or [] # <-- Use the instance

    task = next((t for t in tasks if t['id'] == task_id), None)

    if task:
        task['completed'] = data.get('completed', task['completed'])
        # Save the modified list back to Vercel KV
        kv_store.set('tasks', tasks) # <-- Use the instance
        return jsonify(task)

    return jsonify({"error": "Task not found"}), 404

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Endpoint to delete a task from Vercel KV."""
    tasks = kv_store.get('tasks') or [] # <-- Use the instance

    task_found = any(t['id'] == task_id for t in tasks)

    if task_found:
        # Create a new list excluding the task to be deleted
        tasks = [t for t in tasks if t['id'] != task_id]
        # Save the new list back to Vercel KV
        kv_store.set('tasks', tasks) # <-- Use the instance
        return jsonify({"success": "Task deleted"})

    return jsonify({"error": "Task not found"}), 404

# This main block is not used by Vercel but is good for local testing
if __name__ == '__main__':
    app.run(debug=True)
