from django.db import models
from users.models import MyUsers as User


class ChatRoom(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_room')
    fellow_user = models.ForeignKey(User, on_delete=models.CASCADE) 

    @property
    def fellow_user_data(self): 
        return User.objects.get(id=self.fellow_user.id) 
    
    @property
    def last_message(self): 
        message1_set = self.message1.all() 
        message2_set = self.message2.all() 
        messages = message1_set.union(message2_set).order_by('-date')[:1].values()
        return list(messages)
    
    @property
    def messages(self): 
        message1_set = self.message1.all() 
        message2_set = self.message2.all() 
        messages = message1_set.union(message2_set).values()
        return list(messages)
    
    def __str__(self): 
        return self.user.username + ' to ' + self.fellow_user.username


class Message(models.Model): 
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.CharField(max_length=1000) 
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    room1 = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='message1', null=True)
    room2 = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='message2', null=True)

    class Meta: 
        ordering = ['date']

    @property
    def sender_data(self): 
        return User.objects.get(id=self.sender.id) 
    
    @property
    def receiver_data(self): 
        return User.objects.get(id=self.receiver.id)
    
    def __str__(self): 
        return self.message 
    

