from django.urls import path 
from . import views

urlpatterns = [
    path('get_chats/', views.GetAvailableChats.as_view()), 
    path('get_messages/', views.GetMessages.as_view()), 
    path('get_room/', views.GetRoom.as_view()), 
]
