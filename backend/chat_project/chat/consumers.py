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















# import json
# from channels.generic.websocket import WebsocketConsumer

# class ChatConsumer(WebsocketConsumer):

#     def connect(self):
#         self.accept()

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']

#         self.send(text_data=json.dumps({
#             'message': message
#         }))
