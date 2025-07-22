# Todo List Web Application

A simple, clean, and functional todo list web application built with a Python Flask backend and a vanilla JavaScript frontend.

You can view the live, deployed version of this application here:
# Test my application [Mohit's Todo App](https://mohit-to-do-list-app.onrender.com/) 📝
# Test my application [Mohit's Todo App](https://mohit-to-do-list-app.onrender.com/) 📝

## Features

- **Add Tasks:** Quickly add new tasks to your list.
- **View Tasks:** See all your tasks in a clean, organized list.
- **Complete Tasks:** Mark tasks as complete with a satisfying checkmark.
- **Delete Tasks:** Remove tasks you no longer need.
- **Persistent Storage:** Tasks are managed by the Flask backend and stored in memory on the server.

## Tech Stack

- **Frontend:**
  - HTML5
  - Tailwind CSS (for styling)
  - Vanilla JavaScript (for interactivity and API calls)
- **Backend:**
  - Python
  - Flask (as the web framework and API server)
  - Gunicorn (as the production web server)
- **Deployment:**
  - Render

## Local Installation and Setup

For developers who wish to run this project on their local machine, please follow these steps:

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create a Virtual Environment**
    It's recommended to use a virtual environment to keep project dependencies separate.
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    This project's required Python packages are listed in the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask Application**
    ```bash
    python backend.py
    ```

5.  **View the Application**
    Open your web browser and navigate to the local development server:
    ```
    [http://127.0.0.1:5000](http://127.0.0.1:5000)
    ```

---
*This project was built by Mohit Kumar Panigrahi.*
