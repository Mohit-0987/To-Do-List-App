# Import necessary libraries
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from vercel_kv import KV
import time
import os

# Create a Flask application instance
app = Flask(__name__)
CORS(app)

# --- Manual Override for Debugging ---
# Replace the placeholder text with the actual values from your Vercel settings.
kv_store = KV(
    url="rediss://default:AeyrAAIjcDE5YTNhMWMwYzU5ZTM0MTQyODZlZWM2ZDY2NzRjMjRkOXAxMA@measured-silkworm-60587.upstash.io:6379",
    rest_api_url="https://measured-silkworm-60587.upstash.io",
    rest_api_token="AeyrAAIjcDE5YTNhMWMwYzU5ZTM0MTQyODZlZWM2ZDY2NzRjMjRkOXAxMA",
    rest_api_read_only_token="AuyrAAIgcDFXBwNL0AyqnmF7FTvvd72iSEH18zvZ2V8z3YfEFELgNw"
)


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
