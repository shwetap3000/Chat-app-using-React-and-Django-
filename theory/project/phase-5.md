Now we start **Phase 5 — Real-Time Messaging using WebSockets and Django Channels**.
This phase is the **core of a chat system**, because this is what makes messages appear **instantly without refreshing the page**.

We will go slowly and understand the concepts before writing code.

---

# Phase 5 — WebSockets and Django Channels

In this phase you will understand:
• Why REST APIs cannot power real-time chat
• What WebSockets are
• How WebSockets keep a connection open
• What **Django Channels** does
• What **ASGI** is
• How messages travel between users in real time

Later we will implement:
1. Install Channels
2. Configure ASGI
3. Create WebSocket routing
4. Create a **Chat Consumer**
5. Connect frontend to WebSocket

---

# 1 — Why REST APIs Are Not Enough for Chat

Let’s understand the problem first.

Imagine **User A sends a message to User B**.

### Using normal REST API

Flow would be:
1. User A sends message → POST `/send-message`
2. Server saves message
3. User B needs to **refresh or request again** to see new messages

Example:
Frontend keeps asking server:
```
GET /messages/
GET /messages/
GET /messages/
GET /messages/
```

This is called **polling**.

Problems with polling:
• Waste of server resources
• Slow message delivery
• Not real-time
• Bad user experience

Messaging apps like:
* WhatsApp
* Discord
* Slack
cannot work like this.
They need **instant delivery**.

---

# 2 — Solution: WebSockets

WebSockets solve this problem.
Instead of opening and closing connections like HTTP, WebSockets create a **persistent connection**.

*(a network communication method where a single TCP connection stays open to handle multiple HTTP requests and responses, rather than closing after each exchange is know as the persistent connection)*

Normal HTTP:
```
Client → request
Server → response
Connection closes
```

WebSocket:
```
Client ⇄ Server
Connection stays OPEN
```
This allows **two-way communication**.

Meaning:
• Client can send messages
• Server can send messages anytime

---

# 3 — How Chat Works With WebSockets

Let’s see the real flow.

### Step 1 — User opens chat

React frontend opens a WebSocket connection:
```
ws://localhost:8000/ws/chat/1/
```
Here `1` = conversation id.

---

### Step 2 — Server joins user to a chat room

The server creates something like:
```
room_1
```
Both users in that conversation join the same room.

---

### Step 3 — User sends message

User A sends message through WebSocket:
```
Hello
```
Server receives message.

---

### Step 4 — Server broadcasts message

Server sends message to **all users in that room**.
```
User A receives message
User B receives message
```
This happens **instantly**.

---

# 4 — What Django Channels Does

Django normally works with **HTTP requests only**.
It cannot handle WebSockets.

So we use:
### Django Channels

Django Channels adds support for:
• WebSockets
• background tasks
• long connections
• async communication

Think of it like this:
```
Normal Django → handles HTTP
Django Channels → handles WebSockets
```

---

# 5 — What is ASGI

Before Channels, Django used:
```
WSGI
```

WSGI supports only:
```
HTTP
```

But WebSockets require:
```
asynchronous connections
```

So Django introduced:
```
ASGI (Asynchronous Server Gateway Interface)
```

ASGI allows:
• HTTP
• WebSockets
• async communication

Channels works on top of **ASGI**.

---

# 6 — What Redis Does in Chat Systems

In a chat system, we must manage **rooms and message broadcasting**.

Example:
```
Conversation 1 → User A + User B
Conversation 2 → User C + User D
```

When a message arrives:
```
send to everyone in room
```

Django Channels uses something called a **Channel Layer**.

This layer manages:
• chat rooms
• message broadcasting
• communication between processes

The most common channel layer backend is:
```
Redis
```
Redis acts like a **fast in-memory message broker**.

Flow:
```
User sends message
      ↓
Django Channels
      ↓
Redis distributes message
      ↓
All users in the room receive it
```

*Redis has a feature called Publish/Subscribe.When User A sends a message, the server publishes it to Redis.Redis immediately sends the message to all users subscribed to that chat.This makes messages appear instantly.*

---

# 7 — Final Architecture After Adding Channels

Your chat system now looks like this:
```
React Frontend
      │
      │ REST APIs
      ▼
Django REST Framework
      │
      │ database operations
      ▼
Database (PostgreSQL / SQLite)



Real-time layer
-----------------

React WebSocket
      │
      ▼
Django Channels
      │
      ▼
Redis
      │
      ▼
Other connected users
```

---

# 8 — What We Will Build in the Next Steps

Now that you understand the architecture, we will start **implementing the real-time system**.

Next steps will be:

### Step 1
Install required packages
```
channels
channels-redis
daphne
```

### Step 2
Configure Channels in Django.

### Step 3
Create **WebSocket routing**.

### Step 4
Create a **Chat Consumer** (WebSocket handler).

### Step 5
Connect React frontend to WebSocket.

---

# Before We Start Coding Phase 5

I want to make sure you clearly understand one key idea:
What is the **biggest difference between REST API communication and WebSocket communication** in a chat application?

Explain it in your own words.





Now we move to **Phase 5 — Part 2: Installing and Configuring Django Channels**.
This is the step where your Django project becomes capable of handling **WebSockets**.

In this part we will do four things:
1. Install required packages
2. Add Channels to Django
3. Configure ASGI
4. Configure the Channel Layer (Redis)

For now we will focus on **understanding and configuring**, not building the chat logic yet.

---

# 1 — Install Required Packages

Django alone cannot handle WebSockets, so we install additional packages.

Run this in your project environment:
```bash
pip install channels channels-redis daphne
```

Now let’s understand what each package does.

### channels

This is the main package that adds **WebSocket support to Django**.

It allows Django to work with:
* WebSockets
* background workers
* asynchronous communication

*Asynchronous communication = sending a request and continuing other work without waiting for the response*

Without this package, Django only understands **HTTP requests**.

---

### channels-redis

This package connects Django Channels with **Redis**.

Redis is used as a **channel layer** to manage:
* chat rooms 
* message broadcasting
* communication between users

*A channel layer is a message system that lets different parts of a real-time app communicate with each other, and Redis is often used to power it.*

Example idea:
If two users are in the same conversation, Redis helps send the message to **everyone inside that conversation room**.

---

### daphne

Daphne is an **ASGI server**.

Remember earlier we discussed:
WSGI → used for HTTP
ASGI → used for WebSockets

Daphne is the server that runs Django using **ASGI instead of WSGI**.
(normal django app runs using wsgi).

---

# 2 — Add Channels to Installed Apps

Open:
`settings.py`

Find:
```python
INSTALLED_APPS = [
```

Add Channels to the list.

```python
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'channels',

    'chat',
]
```
Now Django knows that **Channels is part of the project**.

---

# 3 — Configure ASGI Application

Still in `settings.py`, add this line:
```python
ASGI_APPLICATION = "chatproject.asgi.application"
```

Explanation:
This tells Django that the project will run using **ASGI instead of WSGI**.

ASGI is necessary for:
* WebSockets
* asynchronous tasks
* long-lived connections

---

# 4 — Understanding the `asgi.py` File

When you created the Django project, Django automatically created a file:
```
chatproject/asgi.py
```

This file defines **how the server handles connections**.

Open it and you will see something like:
```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatproject.settings')

application = get_asgi_application()
```

Currently this file only handles **HTTP requests**.

Later we will modify it to handle:
* HTTP requests
* WebSocket connections

At that point the server will know **how to route WebSocket traffic**.

---

# 5 — Configure the Channel Layer (Redis)

Now we tell Django Channels to use **Redis**.

In `settings.py`, add:
```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

Explanation:

`BACKEND`
This tells Django Channels to use Redis as the communication layer.

`hosts`
This is where Redis is running.

Default Redis port:
```
6379
```

---

# 6 — Why Redis Is Needed

Imagine three users in a conversation.
```
User A
User B
User C
```

User A sends a message.
Without Redis the server would struggle to broadcast the message efficiently.

With Redis:
```
User A → Django Channels
           ↓
         Redis
           ↓
User B receives message
User C receives message
```

Redis acts like a **fast message distributor**.

---

# 7 — What We Achieved in This Part

Your project now has the **real-time infrastructure**.

You installed:
* Channels
* Redis integration
* Daphne server

You configured:
* ASGI support
* Channel layers

But the project still cannot handle WebSockets yet because we still need:
• WebSocket routing
• Consumers (WebSocket handlers)

Those will be implemented next.

---

# Next Part (Phase 5 — Part 3)

We will create the **WebSocket system itself**.

You will build:
1. `routing.py`
2. a **ChatConsumer**
3. WebSocket URL patterns

This is where you will finally see **how messages travel through WebSockets**.






Good. Now we move to **Phase 5 — Part 3: Creating the WebSocket System**.
This is where we actually build the components that allow **real-time chat communication**.

In this part we will create three important things:
1. **Consumer** (WebSocket handler)
2. **WebSocket routing**
3. **ASGI configuration update**

These three components together allow Django to **receive and send WebSocket messages**.

---

# 1 — Understanding What a Consumer Is

In Django Channels, a **Consumer** plays the same role as a **View** in REST APIs.

Comparison:

REST API
```
Client → View → Response
```

WebSocket
```
Client → Consumer → WebSocket response
```

A **Consumer** is responsible for:
* accepting WebSocket connections
* receiving messages
* sending messages
* handling connection closing
Think of it as a **WebSocket controller**.

---

# 2 — Create the Consumer File

Inside your **chat app**, create a new file:
```
chat/consumers.py
```

Add the following code.

```python
import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
```

---

# 3 — Understanding This Code

Let’s break it down carefully.

### Import section

```python
from channels.generic.websocket import WebsocketConsumer
```

`WebsocketConsumer` is a class provided by **Django Channels** that handles WebSocket connections.

We inherit from it to create our own consumer.

---

### `connect()` method

```python
def connect(self):
    self.accept()
```

This runs **when a client tries to connect to the WebSocket**.

`self.accept()` means:
The server **accepts the connection**.

Without this line the WebSocket connection will be rejected.

---

### `receive()` method

```python
def receive(self, text_data):
```

This method runs **whenever the client sends data through the WebSocket**.

Example message sent from frontend:

```json
{
  "message": "Hello"
}
```

---

### Convert JSON to Python

```python
data = json.loads(text_data)
```

WebSocket messages arrive as **JSON strings**, so we convert them to Python objects.

---

### Extract message

```python
message = data['message']
```

Now we extract the actual chat message.

---

### Send response back

```python
self.send(text_data=json.dumps({
    'message': message
}))
```

The server sends the same message back.

This is just a **simple echo system** to confirm WebSockets are working.

Later we will:
* save messages in the database
* broadcast messages to other users

---

# 4 — Create WebSocket Routing

Now we define **WebSocket URLs**, similar to how Django has `urls.py` for HTTP.

Inside the **chat app**, create:
```
chat/routing.py
```

Add this code.

```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]
```

Explanation:

`ws/chat/` is the **WebSocket endpoint**.

Frontend will connect using:
```
ws://localhost:8000/ws/chat/
```

---

# 5 — Update the ASGI File

Now we connect WebSocket routing with the Django project.

Open:
```
projectname/asgi.py
```

Replace the content with:

```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectname.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
```

---

# 6 — Understanding the ASGI Configuration

This file now tells Django how to route connections.

### ProtocolTypeRouter

This decides **what type of connection is incoming**.
```
HTTP request → normal Django
WebSocket → Channels routing
```

---

### URLRouter

Routes WebSocket requests to the correct **consumer**.

Example:
```
ws/chat/ → ChatConsumer
```

---

### AuthMiddlewareStack

This enables **user authentication inside WebSockets**.

So later we can know:
```
which user sent the message
```

---

# 7 — What Happens Now

When a user connects to:
```
ws://localhost:8000/ws/chat/
```

The flow becomes:

```
React client
      ↓
ASGI server
      ↓
ProtocolTypeRouter
      ↓
WebSocket routing
      ↓
ChatConsumer
```

The consumer now:
* accepts connection
* receives messages
* sends responses

---

# 8 — Testing the WebSocket

Your Django server should now run normally:
```
python manage.py runserver
```

But browsers cannot easily test WebSockets directly.

Later when we connect **React**, we will see the messages instantly.

---

# What We Achieved in Phase 5 Part 3

Your backend now has:
• WebSocket consumer
• WebSocket routing
• ASGI WebSocket configuration

This means your Django project is now **WebSocket capable**.

But the chat is still incomplete because:
* messages are not saved in the database
* messages are not broadcast to multiple users
* chat rooms are not implemented

---

# Next Part (Phase 5 — Part 4)

In the next step we will implement the **real chat logic**:
• join a conversation room
• broadcast messages to all participants
• store messages in the database

This will turn the echo system into a **real multi-user chat system**.






Excellent. Now we move to **Phase 5 — Part 4: Building the Real Chat Logic**.
Until now the WebSocket only **echoed messages back to the same user**. Now we will turn it into a **real multi-user chat system**.

In this step we will implement:
1. **Chat Rooms (Conversation rooms)**
2. **Broadcast messages to all users**
3. **Save messages in the database**
4. **Send messages to everyone in the conversation**

This is the **core mechanism of chat apps**.

---

# 1 — Understanding Chat Rooms

Every conversation must have its **own WebSocket room**.

Example:

Conversation 1
```
User A
User B
```

Conversation 2
```
User C
User D
```

So we create **different WebSocket groups**.

Example group names:
```
chat_1
chat_2
chat_3
```

Where the number is the **conversation ID**.
When a user opens a chat, they join that group.

Flow:
```
User connects
↓
Join group chat_1
↓
Send message
↓
Server broadcasts to group chat_1
↓
All participants receive message
```

---

# 2 — Update WebSocket Routing

Open:
```
chat/routing.py
```

Modify the URL so that the **conversation id is included**.

```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<conversation_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
```

Now WebSocket URLs look like:
```
ws://localhost:8000/ws/chat/1/
```
Here `1` is the **conversation id**.

---

# 3 — Update the Consumer

Now we rewrite the consumer to support:
* groups
* broadcasting
* database storage

Open:
```
chat/consumers.py
```

Replace the code with this.

```python
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message, Conversation
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):

    def connect(self):

        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"chat_{self.conversation_id}"

        # join room
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):

        # leave room
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    def receive(self, text_data):

        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender']

        conversation = Conversation.objects.get(id=self.conversation_id)
        sender = User.objects.get(id=sender_id)

        # save message to database
        Message.objects.create(
            conversation=conversation,
            sender=sender,
            content=message
        )

        # broadcast message to group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )


    def chat_message(self, event):

        message = event['message']
        sender = event['sender']

        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
```

---

# 4 — Understanding the Important Parts

## Getting conversation ID
```
self.scope['url_route']['kwargs']['conversation_id']
```
This extracts the ID from the WebSocket URL.

Example:
```
ws/chat/1/
```
Conversation id = **1**

---

# Joining a Group
```
self.channel_layer.group_add()
```
This adds the user to a **chat room group**.

Example group:
```
chat_1
```
All users connected to this group receive the same messages.

---

# Saving Messages
```
Message.objects.create(...)
```
Every time a message arrives we store it in the database.
So the chat history is preserved.

---

# Broadcasting Messages
```
self.channel_layer.group_send()
```
This sends the message to **everyone inside the room**.

Example:
```
User A sends message
↓
Server broadcasts
↓
User B receives message instantly
```

---

# Sending Message to Client
```
self.send()
```
This pushes the message back to the frontend.
The frontend will then display the new message.

---

# 5 — Message Flow in the System

Now the full process becomes:
```
User A sends message via WebSocket
↓
ChatConsumer.receive()
↓
Save message in database
↓
Send message to Redis channel layer
↓
Broadcast to group chat_1
↓
All connected users receive message
↓
Frontend updates instantly
```

---

# 6 — Real Architecture Now

Your chat system now works like this:
```
React Frontend
      │
      │ WebSocket
      ▼
Django Channels (Consumer)
      │
      │ broadcast
      ▼
Redis Channel Layer
      │
      ▼
Other connected users

Database
stores chat history
```

---

# 7 — What You Have Built So Far

Your backend now supports:
✔ WebSocket connections
✔ Conversation chat rooms
✔ Real-time message broadcasting
✔ Database message storage

This is essentially the **same architecture used in real chat systems**.

---

# Next Phase

The backend is now almost complete.

The next step is **Phase 6 — Connecting the React Frontend to the WebSocket server**.

In that phase you will learn:

* how React opens WebSocket connections
* how messages are sent
* how real-time UI updates happen

---

Before we move there, I want to check something important for correctness.

In the consumer we used:

```
async_to_sync(self.channel_layer.group_add)
```

Do you understand **why we needed `async_to_sync` here?**

This concept is very important in Django Channels.
