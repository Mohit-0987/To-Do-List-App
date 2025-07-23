# Import necessary libraries
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from vercel_kv import KV
import time
import os # <-- Import the 'os' module

# Create a Flask application instance
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# --- START OF DEBUGGING CODE ---
# We will print the environment variables to the Vercel logs.
print("--- Vercel KV Environment Variable Check ---")
print(f"KV_URL: {os.environ.get('KV_URL')}")
print(f"KV_REST_API_URL: {os.environ.get('KV_REST_API_URL')}")
print(f"KV_REST_API_TOKEN: {os.environ.get('KV_REST_API_TOKEN')}")
print(f"KV_REST_API_READ_ONLY_TOKEN: {os.environ.get('KV_REST_API_READ_ONLY_TOKEN')}")
print("--- End of Check ---")
# --- END OF DEBUGGING CODE ---

# This is the line that is currently failing.
# It will still fail, but the logs before it will give us the information we need.
kv_store = KV()


# --- Route for the Homepage ---
@app.route('/')
def home():
    return render_template('frontend.html')


# --- API Endpoints ---
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = kv_store.get('tasks') or []
    return jsonify(tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.get_json()
    tasks = kv_store.get('tasks') or []
    new_task = {
        "id": int(time.time() * 1000),
        "text": data['text'],
        "completed": False
    }
    tasks.append(new_task)
    kv_store.set('tasks', tasks)
    return jsonify(new_task), 201

@app.route('/update_task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    tasks = kv_store.get('tasks') or []
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        task['completed'] = data.get('completed', task['completed'])
        kv_store.set('tasks', tasks)
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = kv_store.get('tasks') or []
    tasks = [t for t in tasks if t['id'] != task_id]
    kv_store.set('tasks', tasks)
    return jsonify({"success": "Task deleted"})
