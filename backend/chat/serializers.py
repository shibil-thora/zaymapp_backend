from rest_framework import serializers 
from .models import Message, ChatRoom
from users.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer): 
    sender_data = UserSerializer(read_only=True)
    receiver_data = UserSerializer(read_only=True) 


    class Meta: 
        model = Message 
        fields = [
            'id'
            'sender', 
            'receiver', 
            'message', 
            'is_read', 
            'date', 
            'sender_data', 
            'receiver_data', 
        ]

class ChatRoomSerializer(serializers.ModelSerializer): 
    fellow_user_data = UserSerializer(read_only=True)

    class Meta: 
        model = ChatRoom
        fields = ['id', 'user', 'fellow_user', 'fellow_user_data', 'last_message', 'messages']