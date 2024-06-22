from django.db import models
from django.contrib.auth.models import AbstractUser 


class MyUsers(AbstractUser): 
    is_provider = models.BooleanField(default=False)  
    is_premium = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics',)


class Notification(models.Model): 
    informer = models.ForeignKey(MyUsers, on_delete=models.CASCADE)
    receiver = models.ForeignKey(MyUsers, on_delete=models.CASCADE, related_name='notifications') 
    message = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True) 

    @property 
    def informer_data(self): 
        return self.informer 
    
    def __str__(self): 
        return self.message