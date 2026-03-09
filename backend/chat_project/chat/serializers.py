from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Conversation, Message

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            # password will not appear in API responses
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # ensures the password is hashed securely
        user = User.objects.create_user(**validated_data)
        return user


# Conversation serializer
class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at']


# Message serializer
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'timestamp']