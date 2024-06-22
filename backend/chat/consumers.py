import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from .models import Message, ChatRoom
from .serializers import MessageSerializer
from users.models import MyUsers as User 
from channels.db import database_sync_to_async
from users.models import Notification


class ChatConsumer(AsyncWebsocketConsumer): 
    async def connect(self): 
        scope = str(self.scope['query_string'])
        f, t = scope.split('&')
        fellow_user_id = f[4:] 
        token = t[2:-1]   
        decoded_token = AccessToken(token) 
        user_id = decoded_token['user_id']  
        
        #developing unique room name using their id 
        id_list = sorted([str(user_id), str(fellow_user_id)]) 
        room_name = "room" + "".join(id_list) 
       
        self.chat_box_name = room_name
        self.group_name = f'chat_{self.chat_box_name}'

        await self.channel_layer.group_add(self.group_name, self.channel_name) 
        await self.accept() 

    async def disconnect(self, close_code): 
        await self.channel_layer.group_discard(self.group_name, self.channel_name) 

    async def receive(self, text_data): 
        text_data_json = json.loads(text_data) 
        # this is the place where we get the data sent from the frontend 
        message = text_data_json["message"] 
        sender_id = text_data_json["sender_id"]  
        receiver_id = text_data_json["receiver_id"] 

        sender = await database_sync_to_async(User.objects.get)(id=sender_id) 
        receiver = await database_sync_to_async(User.objects.get)(id=receiver_id) 
        room1 = await database_sync_to_async(ChatRoom.objects.get)(user=sender, fellow_user=receiver)
        room2 = await database_sync_to_async(ChatRoom.objects.get)(user=receiver, fellow_user=sender)
        message_obj = await database_sync_to_async(Message.objects.create)(
            sender=sender,  
            receiver=receiver, 
            message=message, 
            room1=room1, 
            room2=room2, 
        )  
        notification_obj = await database_sync_to_async(Notification.objects.create)(
            informer=sender, 
            receiver=receiver, 
            message=f'{sender.username} sent you a message'
        )

        await self.channel_layer.group_send(
            self.group_name, 
            {
                'type': 'chatbox_message', 
                'message': { 
                    'id': message_obj.id,
                    'sender_id': sender_id, 
                    'receiver_id': receiver_id, 
                    'message': message,  
                    'date': message_obj.date.isoformat(),
                    'room1': message_obj.room1.id, 
                    'room2': message_obj.room2.id,
                }, 
                'sender_id': sender_id
            },
        ) 

    async def chatbox_message(self, event): 
        message = event["message"]
        sender_id = event["sender_id"]

        await self.send(text_data=json.dumps({"message": message, "sender_id": sender_id}))
