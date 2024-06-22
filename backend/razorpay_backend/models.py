from django.db import models
from users.models import MyUsers as User


class Transaction(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction')
    payment_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    signature = models.CharField(max_length=200)
    amount = models.IntegerField() 
    datetime = models.DateTimeField(auto_now_add=True) 