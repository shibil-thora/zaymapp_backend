from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer, Message, ChatRoomSerializer, ChatRoom
from django.db.models import Q , Count
from users.models import MyUsers as User
from .serializers import ChatRoom, ChatRoomSerializer
from services.models import KnockedUsers
from users.models import Notification


class GetAvailableChats(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request): 
        user = request.user 
        chat_list_objs = user.chat_room.all() 
        chat_list = ChatRoomSerializer(chat_list_objs, many=True).data
        return Response(chat_list) 
    

class GetMessages(APIView): 
    permission_classes = [IsAuthenticated] 
    def post(self, request): 
        chat_id = request.data['chat_id'] 
        chat_obj = ChatRoom.objects.get(id=chat_id)  
        Notification.objects.filter(informer=chat_obj.fellow_user).delete()
        chat = ChatRoomSerializer(chat_obj).data
        return Response(chat) 
    

class GetRoom(APIView): 
    permission_classes = [IsAuthenticated] 
    def post(self, request): 
        user = request.user
        fellow = User.objects.get(id=request.data['user_id'])  
        try:
            KnockedUsers.objects.filter(id=request.data['knock_id']).delete()
        except: 
            pass

        try:
            room = ChatRoom.objects.get(user=user, fellow_user=fellow)  
        except: 
            room = ChatRoom.objects.create(user=user, fellow_user=fellow) 
            ChatRoom.objects.create(user=fellow, fellow_user=user)

        return Response(room.id)