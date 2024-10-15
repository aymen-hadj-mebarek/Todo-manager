# Flask Task Manager Application

This project is a simple **Task Management Web Application** built using **Flask** and **SQLite**. The main objective of this project was to practice building a web application using Flask, setting up user authentication, and managing tasks with a relational database. It includes features like user signup, login, creating and updating tasks, and organizing tasks with due dates.

## Features

- **User Authentication:**
    
    - Sign up with name, email, and password
    - Log in and log out functionality using Flask sessions
    - Password validation
- **Task Management:**
    
    - Users can add, update, and delete tasks
    - Each task has a description, due date, and completion status
    - Tasks are user-specific and displayed only to the logged-in user
    - A checkbox to mark tasks as completed or not completed
- **Task Overview:**
    
    - Tasks are displayed on the homepage with a filter based on the current user
    - Tasks that are overdue are highlighted
    - Option to delete tasks when completed

## Technologies Used

- **Backend Framework:** Flask (Python)
- **Database:** SQLite (via SQLAlchemy)
- **Frontend:** HTML, CSS
- **Session Management:** Flask-Session
- **Templating Engine:** Flask's Jinja2

## Installation and Setup

To get started with this project, follow these steps:

1. **Clone the repository**:
    
    ```powershell
    git clone https://github.com/aymen-hadj-mebarek/flask-task-manager.git cd flask-task-manager
    ```
    
2. **Create a virtual environment** (optional but recommended):
    
    ```powershell
    python -m venv venv source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
    
3. **Install required dependencies**: Install the required Python packages using pip:
    
    ```powershell
    pip install -r requirements.txt
    ```
    
4. **Set up the database**: Run the Flask app once to automatically create the SQLite database file:
    
    ```powershell
    python app.py
    ```
    
    If the database file `DataBase.db` doesn't exist, the app will create one in the `instance` folder.
    
5. **Run the Flask development server**: Start the Flask app to access the website locally:
    
    ```powershell
    flask run
    ```
    
    The server will start at `http://127.0.0.1:5000/`.
    
6. **Access the app**: Open your browser and visit the local URL to use the task manager:
    
    `http://127.0.0.1:5000/`
    

## How It Works

1. **Sign Up and Login**:  
    Users can create an account using their name, email, and password. Once signed up, they can log in using their credentials. Session management is used to keep the user logged in across different pages.
    
2. **Task Creation**:  
    After logging in, users can create new tasks by specifying the task description and a due date.
    
3. **Task Management**:  
    Users can mark tasks as completed, update the status, or delete tasks that are no longer needed. All tasks are tied to the specific user and are displayed in the tasks page.
    
4. **Logout**:  
    Users can log out, clearing the session and preventing access to tasks without logging back in.
    

## Folder Structure

```powershell
├── app.py                # Main Flask app 
├── templates/            # HTML templates (Signup, Login, Tasks, Home) 
├── static/               # Static files (CSS, Images, etc.) 
├── instance/             # SQLite database file is stored here 
├── requirements.txt      # List of dependencies
└── README.md             # This README file
```

## Future Improvements

- **Task categorization** (e.g., work, personal, urgent)
- **Task prioritization** with different levels of importance
- **Better error handling and feedback** to users on form validation
- **User password encryption** for increased security

## Contributions

This project was primarily for learning purposes, but feel free to contribute to its improvement by submitting pull requests or raising issues!
