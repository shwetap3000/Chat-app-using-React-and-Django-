Phase 4 is where the backend becomes **usable by the frontend**. Until now we only created the **database structure**. Now we will build **APIs** so that React can communicate with Django.

The steps inside Phase 4 are:
1. Understand what an API is
2. Understand Django REST Framework
3. Create serializers
4. Create API views
5. Create URL routes
6. Test APIs

We will start with the **concept first**, then implement.

---

# 1. What an API Is

API stands for **Application Programming Interface**.
In simple terms, an API allows **one program to communicate with another program**.

In our chat system:
React (frontend)
communicates with
Django (backend)

Example:
React sends a request:
```
GET /api/users
```

Django responds with data:
```json
[
  {
    "id": 1,
    "username": "shweta"
  },
  {
    "id": 2,
    "username": "rahul"
  }
]
```

This data format is called **JSON**.
JSON is the standard way APIs send data between frontend and backend.

---

# 2. Why We Use Django REST Framework

Django alone can build web pages, but it is not designed specifically for APIs.
Django REST Framework (DRF) makes API creation easier.

It provides:
* serializers
* API views
* authentication tools
* easy JSON responses

DRF converts **Python objects → JSON responses**.

Example:

Python object
```
User(id=1, username="shweta")
```

API response
```json
{
  "id": 1,
  "username": "shweta"
}
```

This conversion is handled by **serializers**.

---

# 3. What Serializers Do

Serializers convert **database objects into JSON format**.
They also validate incoming data.
Think of a serializer as a **translator between Django models and JSON**.

Example flow:
Database object
→ Serializer
→ JSON response

And also the reverse:
JSON request
→ Serializer
→ Database object

Example request from React:
```json
{
  "username": "rahul",
  "password": "1234"
}
```

Serializer validates it before creating a user.

---

# 4. Creating Serializers

We will create serializers for:
* User
* Conversation
* Message

Inside the **chat app**, create a new file:
```
chat/serializers.py
```

Add the following code.

### User Serializer

```python
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
```

Explanation:
This serializer converts a **User model instance into JSON**.

Example output:
```json
{
  "id": 1,
  "username": "shweta"
}
```

---

### Conversation Serializer

```python
from .models import Conversation

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at']
```

This serializer converts conversations into JSON.

Example output:
```json
{
  "id": 1,
  "participants": [1, 2],
  "created_at": "2026-03-07T10:30:00"
}
```

---

### Message Serializer

```python
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'timestamp']
```

Example response:
```json
{
  "id": 3,
  "conversation": 1,
  "sender": 2,
  "content": "Hello",
  "timestamp": "2026-03-07T10:35:00"
}
```

---

# 5. What Views Do

Views handle **incoming API requests**.

Example request:
```
GET /api/users
```

The view will:
1. receive the request
2. fetch users from the database
3. serialize the data
4. return JSON response

So the flow is:
Client request
→ View
→ Database
→ Serializer
→ JSON response

---

# 6. Creating API Views

Open:
```
chat/views.py
```

Add the following.

### Fetch All Users API

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
```

Explanation:
* `@api_view(['GET'])` → this API only allows GET requests
* `User.objects.all()` → fetch all users from database
* `many=True` → tells serializer we are serializing multiple objects
* `Response()` → returns JSON response

Example response:
```json
[
  {
    "id": 1,
    "username": "shweta"
  },
  {
    "id": 2,
    "username": "rahul"
  }
]
```

---

# 7. Creating URL Routes

Now we connect the API to a URL.

Create a file inside the chat app:
```
chat/urls.py
```

Add:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.get_users),
]
```

Now connect this to the **main project URLs**.

Open:
```
chat_project/urls.py
```

Modify it:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),
]
```

Now the API endpoint becomes:
```
http://127.0.0.1:8000/api/users/
```

---

# 8. Testing the API

Run the server:
```
python manage.py runserver
```

Open the browser:
```
http://127.0.0.1:8000/api/users/
```

You should see JSON data like:
```json
[
  {
    "id": 1,
    "username": "shweta"
  }
]
```

This means the API is working.

---

# What You Learned So Far

You now understand:
* what APIs are
* how frontend and backend communicate
* how serializers convert models to JSON
* how views process requests
* how URL routing connects APIs

---

We will now continue **Phase 4 (Part 2)** where we build the remaining APIs that the frontend will need to operate the chat system.

In this part we will implement:
1. User Registration API
2. User Login API
3. Create Conversation API
4. Get Conversations of a User
5. Fetch Message History

These APIs together will allow the frontend to:
* create accounts
* login
* see other users
* start conversations
* load previous messages

---

# 1 — User Registration API

Purpose:
Allow a new user to **create an account**.

### Step 1 — Update `UserSerializer`

Open:
`chat/serializers.py`

Modify the serializer so that it also accepts a password.

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
```

Explanation:
`write_only=True`
Password will not appear in API responses.

`create_user()`
Ensures the password is **hashed securely**.

---

### Step 2 — Create Registration View

Open:
`chat/views.py`

Add:
```python
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)
```

Flow:
Frontend sends user data → serializer validates → user is created.

Example request:
```json
{
  "username": "rahul",
  "password": "1234"
}
```

---

### Step 3 — Add URL

Open:
`chat/urls.py`

Add:
```python
path('register/', views.register_user),
```

Now the endpoint is:
```
/api/register/
```

---

# 2 — User Login API

Login APIs usually return **authentication tokens**, but for now we will keep a **simple login validation**.

Add this in `views.py`.
```python
from django.contrib.auth import authenticate

@api_view(['POST'])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user:
        return Response({"message": "Login successful", "user_id": user.id})

    return Response({"error": "Invalid credentials"})
```

Explanation:
`authenticate()` checks username and password against the database.

If correct → user logged in.

---

### Add URL

In `chat/urls.py`
```python
path('login/', views.login_user),
```

Endpoint:
```
/api/login/
```

---

# 3 — Create Conversation API

Purpose:
Start a chat between two users.

Add in `views.py`:
```python
from .models import Conversation
from django.contrib.auth.models import User
from .serializers import ConversationSerializer

@api_view(['POST'])
def create_conversation(request):
    user_ids = request.data.get('participants')

    # user is a query set of User object
    users = User.objects.filter(id__in=user_ids)

    conversation = Conversation.objects.create()

    # attach these users to this conversation
    # Use set() when you want the relationship to exactly match a given list.
    # Use add() when you want to append new items without removing old ones.
    conversation.participants.set(users)

    serializer = ConversationSerializer(conversation)

    return Response(serializer.data)
```

Example request:
```json
{
  "participants": [1,2]
}
```

Meaning:
Create conversation between user 1 and user 2.

---

### Add URL

In `chat/urls.py`
```python
path('conversations/create/', views.create_conversation),
```

---

# 4 — Get Conversations of a User

Purpose:
When a user logs in, they should see **all conversations they belong to**.

Add in `views.py`:

```python
# view to handle the get request only
@api_view(['GET'])

# function to get all the conversation of a specific user (hence we have used a specific user id)
def get_conversations(request, user_id):

    # getting this user from the database whose id is user_id
    user = User.objects.get(id=user_id)

    # get all conversation of that user (here this will work bcoz in the models we have already defined the many-to-many field relation)
    conversations = user.conversations.all()

    # here we are serializing many conversation hence we have used many=True
    serializer = ConversationSerializer(conversations, many=True)

    # sending data back to the client
    return Response(serializer.data)
```

Explanation:

We use:
```
user.conversations.all()
```

This works because we defined:
```
related_name='conversations'
```
in the Conversation model.

---

### Add URL

In `chat/urls.py`

```python
path('conversations/<int:user_id>/', views.get_conversations),
```

Endpoint example:
```
/api/conversations/1/
```

---

# 5 — Fetch Message History

Purpose:
Load previous messages when a user opens a chat.

Add in `views.py`.

```python
from .models import Message
from .serializers import MessageSerializer

@api_view(['GET'])
def get_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id)

    serializer = MessageSerializer(messages, many=True)

    return Response(serializer.data)
```

Example endpoint:
```
/api/messages/1/
```

This will return all messages of conversation 1.

---

### Add URL

In `chat/urls.py`
```python
path('messages/<int:conversation_id>/', views.get_messages),
```

---

# Final API List

After Phase 4 your backend should support these APIs:

Fetch users
```
GET /api/users/
```

Register user
```
POST /api/register/
```

Login user
```
POST /api/login/
```

Create conversation
```
POST /api/conversations/create/
```

Get user conversations
```
GET /api/conversations/<user_id>/
```

Fetch message history
```
GET /api/messages/<conversation_id>/
```

---


You now understand:
* serializers convert models ↔ JSON
* views handle API logic
* URL routes expose endpoints
* frontend will call these APIs using **Axios**

At this point the **backend is capable of managing chat data**.
The only missing part is **real-time communication**.

---

The next phase will introduce the **core technology used in chat systems**:

**Phase 5 — WebSockets and Django Channels**

In that phase you will understand:
* why chat cannot rely only on REST APIs
* how WebSocket connections stay open
* how messages are pushed instantly
* how Django Channels manages chat rooms

Before moving there, I want to confirm one important thing:

