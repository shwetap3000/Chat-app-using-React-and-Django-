In this phase we will **build the backend foundation** for the chat system. The goal is not only to run commands but to clearly understand **why each step is done** and **how Django organizes a project internally**.

---

# Step 1 — Create the Project Folder

First create a folder where the backend code will live.

Example structure:
```
chat-app/
   backend/
```

Why do we create a separate backend folder?
Because in a full-stack project we usually have:
```
chat-app/
   backend/   → Django server
   frontend/  → React application
```

This keeps both parts organized.

Now move inside the backend folder.

---

# Step 2 — Create a Virtual Environment

A **virtual environment** is an isolated Python environment.

It ensures that:
* project dependencies do not conflict with other projects
* different projects can use different package versions

Example:
Project A might need Django 4
Project B might need Django 5
Virtual environments allow both to coexist.

Create the virtual environment:
```
python -m venv venv
```

This creates a folder:
```
backend/
   venv/
```

Inside this folder Python stores:
* its own interpreter
* installed packages
* scripts for activation

---

# Step 3 — Activate the Virtual Environment

The virtual environment must be activated before installing packages.

On Windows PowerShell:
```
.\venv\Scripts\Activate
```

On Command Prompt:
```
venv\Scripts\activate
```

After activation you will see something like:
```
(venv) PS C:\backend>
```

The `(venv)` indicates that Python packages will now be installed **inside this environment only**.

---

# Step 4 — Install Required Packages

Now install the main packages needed for the backend.

For our chat system we need:
1. Django → backend framework
2. Django REST Framework → API creation
3. Channels → WebSocket support
4. Channels Redis → communication layer

Install them:
```
pip install django
pip install djangorestframework
pip install channels
pip install channels-redis
```

You can check installed packages using:
```
pip list
```

---

# Step 5 — Create the Django Project

Now we create the main Django project.

Run:
```
django-admin startproject chat_project
```

Now the structure becomes:
```
backend/
   venv/
   chat_project/
       manage.py
       chat_project/
           __init__.py
           asgi.py
           settings.py
           urls.py
           wsgi.py
```

Notice something important.

There are **two folders named `chat_project`**.
This often confuses beginners.
The outer folder is the **project container**.
The inner folder contains **project configuration files**.

---

# Step 6 — Understand Important Core Files

Now we must understand what the main Django files do.

---

# manage.py

This file is used to **interact with the Django project**.

It allows you to run commands like:

Run server
```
python manage.py runserver
```

Create app
```
python manage.py startapp chat
```

Database migration
```
python manage.py migrate
```

Think of `manage.py` as a **control panel for the Django project**.

---

# settings.py

This is the **central configuration file of the project**.
It controls how the project behaves.

Important things defined here include:
Installed apps
```
INSTALLED_APPS
```

Database configuration
```
DATABASES
```

Middleware
```
MIDDLEWARE
```

Static files
```
STATIC_URL
```

Security settings
```
SECRET_KEY
```

Debug mode
```
DEBUG
```

Every Django project heavily relies on `settings.py`.

Later we will also configure here:
* REST framework
* Channels
* Redis
* CORS

---

# urls.py

This file controls **URL routing**.

It tells Django:
“If a user visits this URL, run this view.”

Example:
```
example.com/login
```

The `urls.py` decides **which function handles this request**.

Example structure:
```
urlpatterns = [
    path('admin/', admin.site.urls),
]
```

Later we will add our own API routes here.

---

# wsgi.py

This file is used for **deployment with traditional web servers** like:
* Gunicorn
* Apache
* uWSGI

It helps the server communicate with Django.

For development you rarely touch it.

---

# asgi.py

This file is extremely important for **real-time applications**.

ASGI stands for:
**Asynchronous Server Gateway Interface**

It allows Django to handle:
* WebSockets
* long-lived connections
* asynchronous tasks

Because we are building a **chat application**, this file will be used with **Django Channels**.

---

# Step 7 — Run the Django Server

Now test if everything works.

Go inside the project folder:
```
cd chat_project
```

Run:
```
python manage.py runserver
```

You should see:
```
Starting development server at
http://127.0.0.1:8000/
```

Open that URL in the browser.
If Django is installed correctly you will see the **Django welcome page**.

---

# Step 8 — Create Django Apps

A Django project is divided into **apps**.
Each app represents a **specific feature**.

Example large project structure:
```
project/
   users/
   chat/
   notifications/
   payments/
```

Each app handles its own logic.

For our chat system we will create two apps.

### users app

Handles:
* user registration
* authentication
* user profiles

### chat app

Handles:
* conversations
* messages
* chat logic
* WebSocket communication

Create them:
```
python manage.py startapp users
python manage.py startapp chat
```

Now the structure becomes:
```
chat_project/
   users/
   chat/
   manage.py
   chat_project/
```

---

# Step 9 — Understand Django App Structure

Each Django app contains files like:
```
users/
   admin.py
   apps.py
   models.py
   views.py
   tests.py
```

Important ones are:

### models.py
Defines **database tables**.

Example:
User
Message
Conversation

---

### views.py
Contains **logic for handling requests**.

Example:
Login request
Fetch user list
Send message

---

### admin.py
Allows you to register models in the **Django admin panel**.
Admin panel helps you view database records.

---

### apps.py
Contains configuration for that app.
Usually you don't modify it much.

---

# Step 10 — Register Apps in settings.py

Django must know which apps are part of the project.

Open `settings.py`.

Find:
```
INSTALLED_APPS
```

Add your apps.

Example:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'users',
    'chat',
]
```

Now Django will recognize these apps.

---

# End Result of Phase 2

After completing this phase you will have:
Backend project created
Virtual environment configured
Required packages installed
Django apps created
Project structure understood
Server running successfully

---

# Current Backend Structure

Your project should look like this:
```
backend/
   venv/

   chat_project/
       manage.py

       chat_project/
           settings.py
           urls.py
           asgi.py
           wsgi.py

       users/
           models.py
           views.py

       chat/
           models.py
           views.py
```

---

# What We Will Do in Phase 3

Next we move to **the most important part of backend development**.

Designing the **database models**.

We will design:
User relationships
Conversation structure
Message storage
Database relationships

You will also learn:
ForeignKey
ManyToMany relationships
How chat history is stored

---
