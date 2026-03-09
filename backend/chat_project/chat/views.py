from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from django.contrib.auth import authenticate
from .models import Conversation, Message


# fetching all users api
@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# register view
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


# login view
@api_view(['POST'])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user:
        return Response(
            {
                "message": "Login successful",
                "user_id": user.id
            }
        )
    
    return Response({
        "error": "Invalid login credetials"
    })


# view to create chat room for users
@api_view(['POST'])
def create_conversation(request):
    user_ids = request.data.get("participants")
    users = User.objects.filter(id__in=user_ids)

    conversation = Conversation.objects.create()
    conversation.participants.set(users)

    serializer = ConversationSerializer(conversation)

    return Response(serializer.data)


# view to get all the conversation that a specific user is part of
@api_view(['GET'])
def get_conversations(request, user_id):
    user = User.objects.get(id=user_id)

    conversations = user.conversations.all()

    serializer = ConversationSerializer(conversations, many=True)

    return Response(serializer.data)


# fetch message history

@api_view(['GET'])
def get_messages(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id)

    serializer = MessageSerializer(messages, many=True)

    return Response(serializer.data)












# for create conversation view
"""
from .models import Conversation
from django.contrib.auth.models import User
from .serializers import ConversationSerializer

# this view only accepts post request
@api_view(['POST'])

# this function receives http request and process it. The request usually contain JSON
def create_conversation(request):

    # extracting the participant id
    user_ids = request.data.get('participants')

    # This queries the database (using Django ORM) and gets all users whose IDs are in user_ids
    # now we have User objects
    users = User.objects.filter(id__in=user_ids)

    # this creates a new row in the conversation table
    conversation = Conversation.objects.create()

    # this connects the user with the conversation
    # (Behind the scenes Django fills the many-to-many table)
    conversation.participants.set(users)

    # A serializer converts a Django object into JSON format so it can be sent through the API.
    serializer = ConversationSerializer(conversation)

    # This sends the JSON response back to the client.
    return Response(serializer.data)



We define a POST API using @api_view(['POST']).

The function receives the request.

We extract the participant user IDs from the request data.

We query the database to get User objects with those IDs.

We create a new Conversation.

We link the conversation with those users using the ManyToMany field.

We use a serializer to convert the conversation object into JSON.

We return the JSON response.
"""


# for get all the conversation view
"""
Client sends request:
GET /conversations/1

Backend finds User 1

Backend finds all conversations where User 1 participates

Converts them into JSON

Sends them back
"""