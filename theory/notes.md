# Index:
1. WSGI N ASGI










# 1. WESI N ASGI
### **WSGI (Web Server Gateway Interface)**

WSGI is a **standard way for a Python web server to talk to a Python web application**.

* It was designed for **synchronous** apps (one request handled at a time).
* Commonly used with frameworks like **Django** (traditional setup) and **Flask**.
* Good for **simple websites and APIs**.

**Example WSGI servers:**

* Gunicorn
* uWSGI

---

### **ASGI (Asynchronous Server Gateway Interface)**

ASGI is a **newer standard** that allows Python web apps to handle **asynchronous tasks**.

* Supports **async / await**
* Can handle **multiple connections at the same time**
* Supports **WebSockets, real-time apps, and long connections**

Common frameworks using it:

* FastAPI
* Django (modern versions)

**Example ASGI servers:**

* Uvicorn
* Daphne

---

### **Simple Difference**

| Feature               | WSGI                 | ASGI                              |
| --------------------- | -------------------- | --------------------------------- |
| Type                  | Synchronous          | Asynchronous                      |
| Handles many requests | Not efficiently      | Yes                               |
| Supports WebSockets   | ❌ No                 | ✅ Yes                             |
| Used for              | Traditional web apps | Real-time / high-concurrency apps |
| Introduced            | Earlier              | Newer                             |

---

✅ **In one line:**

* **WSGI = synchronous Python web apps**
* **ASGI = asynchronous Python web apps with real-time support**

---

If you want, I can also show a **very small code example of WSGI vs ASGI** so the difference becomes clearer.
