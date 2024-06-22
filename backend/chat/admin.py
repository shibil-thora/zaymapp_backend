from django.contrib import admin
from .models import Message, ChatRoom


class MessageAdmin(admin.ModelAdmin):  
    list_display = ('sender', 'receiver', 'message',)


admin.site.register(Message, MessageAdmin) 
admin.site.register(ChatRoom)
