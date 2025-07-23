# To-do Application

A simple, clean, and persistent Todo list application built with a Python Flask backend, vanilla JavaScript frontend, and a serverless Redis database (Vercel KV). The entire application is designed for and deployed on Vercel.

### [**Live Demo**](https://your-vercel-url-here.vercel.app/)

**(Remember to replace the link above with your actual Vercel deployment URL!)**

![Todo App Screenshot](https://i.imgur.com/gKj3n4G.png)
*(Pro tip: Replace this image with a screenshot of your own running application!)*

---

## ✨ Features

* **Add Tasks:** Quickly add new tasks to your list.
* **Complete Tasks:** Mark tasks as complete with a satisfying line-through.
* **Delete Tasks:** Remove tasks you no longer need.
* **Persistent Storage:** Your tasks are saved in a cloud database, so they won't disappear when you close the browser.
* **Clean UI:** A modern and responsive interface built with Tailwind CSS.

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
* **Backend:** Python with Flask
* **Database:** Vercel KV (Serverless Redis)
* **Deployment:** Vercel

---

## 🚀 Deployment

This project is configured for easy deployment on Vercel.

1.  **Push to GitHub:** After creating the project with the specified file structure, push it to a GitHub repository.
2.  **Import to Vercel:** Import the repository into your Vercel dashboard. Vercel will automatically detect the configuration in `vercel.json`.
3.  **Connect Vercel KV:** In the project's **Storage** tab on Vercel, create and connect a new KV database. Vercel will handle the environment variables needed to connect.
4.  **Deploy!** Trigger a deployment. Your application will be live.

---

## 🖥️ Running the Project Locally

To run this application on your local machine, follow these steps.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create and Activate a Python Virtual Environment:**
    * **On macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **On Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables for Vercel KV:**
    To connect to your Vercel KV database locally, you need to pull the environment variables from your Vercel project. First, install the Vercel CLI:
    ```bash
    npm install -g vercel
    ```
    Then log in and link your project:
    ```bash
    vercel login
    vercel link
    ```
    Finally, pull the environment variables into a `.env` file:
    ```bash
    vercel env pull .env.local
    ```
    The `vercel-kv` library will automatically use these variables.

5.  **Run the Flask App:**
    ```bash
    flask run
    ```

6.  **View in Browser:**
    Open your web browser and navigate to `http://127.0.0.1:5000`. You should see the application running and connected to your cloud database.
