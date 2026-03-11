Perfect. Now we start **Phase 6 — Connecting the React Frontend to the WebSocket Server**.
Until now we built the **entire backend chat engine**. Now we will build the **frontend part that communicates with it**.

In this phase you will learn:
• how React opens a WebSocket connection
• how messages are sent to the server
• how messages are received instantly
• how the UI updates in real time

We will first build a **very simple chat UI** to test the backend.

---

# 1 — How the Frontend Will Communicate

The frontend will do **two types of communication** with the backend.

### REST APIs (HTTP)

Used for:
* user login
* user list
* conversation list
* message history

Example request:
```id="a6cr4g"
GET /api/messages/1/
```

---

### WebSocket

Used for **real-time messages**.

Example connection:
```id="rtv1ur"
ws://localhost:8000/ws/chat/1/
```

Once this connection is open:
* frontend can send messages
* backend can push messages instantly

---

# 2 — Create a React Project (if not already)

If you don’t have one yet, run:
```bash id="34yhjs"
npx create-react-app chat-frontend
```

Then go inside the folder:
```bash id="8r0rba"
cd chat-frontend
```

Start React:
```bash id="x5mtde"
npm start
```

React will run on:
```id="nhqtnl"
http://localhost:3000
```

---

# 3 — Create a Chat Component

Inside `src`, create a file:

```id="8tb8n5"
Chat.js
```

Add the following code.

```javascript id="fdrdc2"
import React, { useState, useEffect } from "react";

function Chat() {

  const [socket, setSocket] = useState(null);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {

    const ws = new WebSocket("ws://localhost:8000/ws/chat/1/");

    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      setMessages((prev) => [
        ...prev,
        data
      ]);
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
    };

    setSocket(ws);

    return () => {
      ws.close();
    };

  }, []);


  const sendMessage = () => {

    socket.send(
      JSON.stringify({
        message: message,
        sender: 1
      })
    );

    setMessage("");
  };


  return (

    <div>

      <h2>Chat</h2>

      <div>
        {messages.map((msg, index) => (
          <p key={index}>
            <b>{msg.sender}:</b> {msg.message}
          </p>
        ))}
      </div>

      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />

      <button onClick={sendMessage}>
        Send
      </button>

    </div>

  );
}

export default Chat;
```

---

# 4 — Use the Chat Component

Open:
```
src/App.js
```

Replace with:

```javascript id="g24y00"
import React from "react";
import Chat from "./Chat";

function App() {
  return <Chat />;
}

export default App;
```

---

# 5 — Understanding the React Code

Now let’s break down the important parts.

---

## Opening the WebSocket

```javascript id="qekf66"
const ws = new WebSocket("ws://localhost:8000/ws/chat/1/");
```

This connects the frontend to the Django WebSocket server.

Conversation id = **1**

---

## Receiving Messages

```javascript id="9x7ktn"
ws.onmessage = (event) => {
```

Whenever the server sends a message, this function runs.

Example data from backend:

```json id="2cmhha"
{
 "message": "Hello",
 "sender": "shweta"
}
```

We store it in state:

```javascript id="4ckmq4"
setMessages((prev) => [...prev, data])
```

This updates the UI instantly.

---

## Sending Messages

```javascript id="lpks9u"
socket.send(JSON.stringify({
  message: message,
  sender: 1
}))
```

This sends the message to the WebSocket server.

---

# 6 — Real-Time Flow Now

Your chat system now works like this:

```id="p0ub85"
React user types message
        ↓
React sends WebSocket message
        ↓
Django Channels Consumer
        ↓
Message saved in database
        ↓
Redis broadcasts message
        ↓
All connected users receive message
        ↓
React UI updates instantly
```

This is **real-time messaging**.

---

# 7 — What You Have Built

You now have a **fully working real-time chat prototype** with:

✔ Django backend
✔ REST APIs
✔ WebSocket communication
✔ Redis broadcasting
✔ React real-time UI

This is already **a complete chat system architecture**.

---

# Next (Final Improvements)

The next improvements will make the system **production-level**.

We can add:

1️⃣ **Authentication with JWT**
2️⃣ **Automatic conversation creation**
3️⃣ **User list UI**
4️⃣ **Conversation switching**
5️⃣ **Typing indicators**
6️⃣ **Online/offline status**
7️⃣ **Message read receipts**
8️⃣ **File/image sharing**

These features are what make apps like **WhatsApp or Discord feel advanced**.

---

Before we continue, tell me one thing so I guide you correctly:

Are you building this **chat system as a learning project**, or are you planning to **integrate it into your NoteKart project**?
