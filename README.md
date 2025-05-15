# 🚀 AutoScheduler Backend

The backend for **AutoScheduler**, a bulk email scheduling and sending application. This Django-based backend leverages **Celery** for asynchronous task management, **Redis** as the message broker, and **Gunicorn** for serving the app in production.

---

https://autoscheduler.in/
![image](https://github.com/user-attachments/assets/bf20dabf-6919-4ecb-bfa6-c0831201e0ee)


## 🧰 Tech Stack

| Tool           | Purpose                                             |
|----------------|-----------------------------------------------------|
| Django         | Web framework for rapid development                 |
| Celery         | Asynchronous task queue for background job handling |
| Redis          | In-memory data store used as a message broker       |
| PostgreSQL     | Database for storing application data               |
| Gunicorn       | WSGI server for serving Django in production        |

---

## ⚙️ Features

- 📧 Schedule and send bulk emails
- 🕒 Background tasks using Celery (e.g., email scheduling)
- 🔧 API for interacting with frontend
- 🛠️ Asynchronous job handling with **Celery** and **Redis**
- 🔐 JWT-based authentication system

---

```bash
# Clone the project repository from GitHub
git clone https://github.com/yourusername/autoscheduler-backend.git
cd autoscheduler-backend

# Set up a virtual environment
python3 -m venv venv

# Activate the virtual environment (Windows)
.\venv\Scripts\activate
# Activate the virtual environment (Linux/macOS)
source venv/bin/activate

# Set up env variables as shown in .env.example

# Install all required dependencies from the `requirements.txt` file
pip install -r requirements.txt

# Apply the migrations to set up the database schema
python manage.py migrate app

# Start the Django development server
python manage.py runserver

# Ensure redis instance is running and run celery
celery -A backend worker --pool=solo --loglevel=info 
```
