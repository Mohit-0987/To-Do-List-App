# Flask & SQLite To-Do List App 📝

A clean, modern, and persistent To-Do list application built with Python, Flask, and SQLite. The frontend is styled with Tailwind CSS for a responsive and attractive user interface.

---

##  [Test My Application](https://to-do-list-app-2hm0.onrender.com target= "blank") 👨🏻‍🎓📝✅
### ⚠️ A Note on Loading Time

> **This website can take up to 30 seconds to load initially. Please be patient.**

This delay is because the application is hosted on a free-tier service (render). These services put applications to "sleep" after a period of inactivity to conserve resources. The first request will "wake up" the application, causing a one-time startup delay.

---

## ✨ Features

* **Add Tasks**: Quickly add new tasks to your list.
* **View Tasks**: See all your current tasks in a clean layout.
* **Mark as Complete**: Click the checkbox to mark tasks as done.
* **Delete Tasks**: Remove tasks you no longer need.
* **Persistent Storage**: Uses an SQLite database to save your tasks, so they are not lost when the server restarts.
* **Responsive Design**: Looks great on both desktop and mobile devices.
* **Modern UI**: Features smooth animations and a visually appealing design.

---

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **Database**: SQLite
* **Frontend**: HTML, Tailwind CSS, JavaScript
* **Deployment Server**: Gunicorn

---

## 🚀 How to Run Locally

Follow these steps to get the application running on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    py -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask application:**
    ```bash
    python to-do.py
    ```

5.  Open your web browser and navigate to `http://127.0.0.1:5000`. The `todo.db` database file will be created automatically in the project directory.
