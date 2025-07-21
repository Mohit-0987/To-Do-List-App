# Import necessary libraries from Flask
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Create a Flask application instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# --- In-Memory Data Storage ---
# We now start with an empty list so the user begins with a clean slate.
tasks = []
# The ID for the first task will now be 1.
next_id = 1

# --- Route for the Homepage ---
@app.route('/')
def home():
    """
    This function runs when someone visits the main URL.
    It tells Flask to find 'frontend.html' in the 'templates' folder and show it.
    """
    return render_template('frontend.html')


# --- API Endpoints (Routes) ---

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Endpoint to get all tasks."""
    return jsonify(tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    """Endpoint to add a new task."""
    global next_id
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Task text is required"}), 400

    new_task = {
        "id": next_id,
        "text": data['text'],
        "completed": False
    }
    tasks.append(new_task)
    next_id += 1
    return jsonify(new_task), 201

@app.route('/update_task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Endpoint to update a task's completion status."""
    data = request.get_json()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        task['completed'] = data.get('completed', task['completed'])
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Endpoint to delete a task."""
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        tasks = [t for t in tasks if t['id'] != task_id]
        return jsonify({"success": "Task deleted"})
    return jsonify({"error": "Task not found"}), 404

# When deploying to a service like Render, the server is started by Gunicorn,
# so this __main__ block is not strictly necessary for production but is good practice to keep.
if __name__ == '__main__':
    # The production server (Gunicorn) will be used instead of this.
    app.run(debug=False)
