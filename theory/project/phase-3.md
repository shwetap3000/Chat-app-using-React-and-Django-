Phase 3 is one of the **most important phases** of building the chat system. If the **database design is correct**, the rest of the system becomes much easier to build. If the database design is poor, many problems appear later.

In this phase we will understand:
* how users are related to conversations
* how messages are related to users
* how chat history is stored
* why we use ForeignKey and ManyToMany relationships

We will first understand the **conceptual design**, and only after that we will implement the models.

---

# 1. What Data a Chat Application Must Store

Think about what information a chat application needs to store permanently.

At minimum we must store three types of data:
1. Users
2. Conversations (or chat rooms)
3. Messages

Let us understand each of them.

---

# 2. User Model
A **User** represents a person using the application.

Typical user data includes:
* id
* username
* email
* password
* date joined

Django already provides a **built-in User model** through its authentication system.

So we do **not need to create our own User model initially**. We can use Django’s built-in one.

This saves time and gives us authentication features.

---

# 3. Conversation (or Chat Room)
A **conversation** represents a chat between users.
In our system we are building **one-to-one chat**.

That means:
One conversation contains **two users**.

Example:
Conversation 1
Participants → Shweta, Rahul

Conversation 2
Participants → Shweta, Aman

So the conversation model must store:
* conversation id
* participants
* creation time

But here we encounter an important design question.

How do we store **multiple users inside one conversation**?

This is where **ManyToMany relationships** come into play.

---

# 4. ManyToMany Relationship

A **ManyToMany relationship** means:
Many records from one table can relate to many records from another table.

Example:
Users ↔ Conversations
A user can participate in many conversations.
A conversation can contain multiple users.

Example:
User table
| id | username |
| -- | -------- |
| 1  | Shweta   |
| 2  | Rahul    |
| 3  | Aman     |

Conversation table
| id  |
| --- |
| 101 |
| 102 |

Relationship table (automatically created)

| user_id | conversation_id |
| ------- | --------------- |
| 1       | 101             |
| 2       | 101             |
| 1       | 102             |
| 3       | 102             |

Meaning:
Conversation 101 → Shweta and Rahul
Conversation 102 → Shweta and Aman

Django handles this automatically when we use **ManyToManyField**.

---

# 5. Message Model
The **Message model** stores each message sent in the chat.

Each message must contain:
* message id
* sender
* conversation
* message content
* timestamp

Now think about the relationships.

Each message:
* belongs to **one conversation**
* is sent by **one user**

So we use **ForeignKey relationships**.

---

# 6. ForeignKey Relationship

A **ForeignKey** means:
Many records in one table refer to **one record in another table**.

Example:
Conversation → Message
One conversation contains many messages.

Example database:
Conversation

| id  |
| --- |
| 101 |

Message
| id | conversation_id | sender_id | text  |
| -- | --------------- | --------- | ----- |
| 1  | 101             | 1         | Hello |
| 2  | 101             | 2         | Hi    |

Here:
conversation_id is a **foreign key** referencing the conversation table.
sender_id is a **foreign key** referencing the user table.

---

# 7. Final Relationship Structure

Now let us combine everything.

User
↔ Conversation (ManyToMany)

Conversation
→ Message (OneToMany)

User
→ Message (OneToMany)

Graphically it looks like this:

User
↕
Conversation
↓
Message

Explanation:
Users participate in conversations.
Conversations contain messages.
Messages are sent by users.

---

# 8. Database Tables Overview

If we translate this design into database tables, it looks like this.

User Table
| id | username | email |
| -- | -------- | ----- |

Conversation Table
| id | created_at |
| -- | ---------- |

Conversation Participants Table (auto-created)
| conversation_id | user_id |
| --------------- | ------- |

Message Table
| id | conversation_id | sender_id | content | timestamp |
| -- | --------------- | --------- | ------- | --------- |

This structure allows us to:
* retrieve all conversations of a user
* retrieve all messages of a conversation
* identify who sent each message

---

# 9. How Chat History Is Stored
When users chat, messages are inserted into the **Message table**.

Example:
Conversation: Shweta ↔ Rahul

Messages stored like this:
| id | conversation | sender | message     | time  |
| -- | ------------ | ------ | ----------- | ----- |
| 1  | 101          | Shweta | Hello       | 10:01 |
| 2  | 101          | Rahul  | Hi          | 10:02 |
| 3  | 101          | Shweta | How are you | 10:03 |

When a user opens the chat window:

The backend simply fetches:
All messages where
conversation_id = 101
Then sends them to React.
React displays them in order.

---

# 10. Why This Structure Works Well

This design has several advantages.
It avoids duplicate data.
Users are stored once.
Messages reference users.
Conversations reference users.
It allows fast queries like:
Get all conversations of a user.
Get all messages of a conversation.
Get sender of a message.

---

# 11. What Models We Will Create

Inside the **chat app**, we will create two models.

Conversation model
Fields:
* participants (ManyToMany with User)
* created_at

Message model
Fields:
* sender (ForeignKey to User)
* conversation (ForeignKey to Conversation)
* content
* timestamp

The **User model** will come from Django’s authentication system.

---

# 12. Concept Check

Before we implement models, make sure these concepts are clear.

Conversation stores **who is chatting**.
Message stores **what was sent**.
ForeignKey connects **messages to conversations and users**.
ManyToMany connects **users to conversations**.

---

In the next step we will actually **implement the models in `models.py`** and then run **database migrations** so Django can create the tables.

Before we write the models, I want to check your understanding with a small question.

If a conversation contains **200 messages**, how many records will exist in the **Message table** for that conversation?


# Step 1 — Import Required Modules

Open `chat/models.py` and at the top write:
```python
from django.db import models
from django.contrib.auth.models import User
```

Explanation:
* `models` → used to create database tables in Django
* `User` → Django’s built-in user model, so we don’t need to create our own

---

# Step 2 — Create Conversation Model

Below the imports, write:
```python
class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"
```

Explanation of each line:

1. `participants = models.ManyToManyField(User, related_name='conversations')`

   * A conversation can have **many users**
   * A user can belong to **many conversations**
   * Django will automatically create a **relationship table** behind the scenes
   * `related_name='conversations'` allows you to do `user.conversations.all()` to get all conversations of a user

2. `created_at = models.DateTimeField(auto_now_add=True)`

   * Stores **when the conversation was created**
   * `auto_now_add=True` means Django automatically sets the timestamp when the record is created

3. `def __str__(self):`

   * Returns a human-readable name for the object
   * Helpful when viewing in **Django admin**

---

# Step 3 — Create Message Model

Right below the Conversation model, write:

```python
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"
```

Explanation of each field:

1. `conversation = models.ForeignKey(...)`

   * Each message belongs to **one conversation**
   * `on_delete=models.CASCADE` → if the conversation is deleted, all messages are deleted too
   * `related_name='messages'` → allows `conversation.messages.all()` to fetch all messages of that conversation

2. `sender = models.ForeignKey(User, on_delete=models.CASCADE)`

   * Each message is sent by **one user**
   * If the user is deleted, their messages are deleted

3. `content = models.TextField()`

   * Stores the **actual message text**

4. `timestamp = models.DateTimeField(auto_now_add=True)`

   * Stores **when the message was sent**

5. `def __str__(self):`

   * Returns first 20 characters of the message along with sender name
   * Helpful for Django admin view

---

# Step 4 — Save the File

Make sure you save `models.py` after writing both models.

---

# Step 5 — Make and Apply Migrations

Now tell Django to **create database tables** based on these models.

Run in terminal:
```bash
python manage.py makemigrations
```

Explanation:
* Django will **generate migration files** describing the new tables

Then run:
```bash
python manage.py migrate
```

Explanation:
* Django will **apply the migrations**, creating tables in the database

---

# Step 6 — Verify in Django Admin (Optional but Helpful)

1. Open `chat/admin.py`
2. Register the models:
```python
from django.contrib import admin
from .models import Conversation, Message

admin.site.register(Conversation)
admin.site.register(Message)
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Run server:
```bash
python manage.py runserver
```

5. Go to `http://127.0.0.1:8000/admin` and check that the models appear

---

✅ After this step:
* Conversation table is ready
* Message table is ready
* Relationships between users, conversations, and messages are correctly set up

---

If you want, the **next step** will be to **create some dummy users and conversations** to test these models and see how messages relate to users in the database.

Do you want to do that next?
