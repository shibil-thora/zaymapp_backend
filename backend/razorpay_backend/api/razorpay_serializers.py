from rest_framework import serializers  
from ..models import Transaction


class CreateOrderSerializer(serializers.Serializer): 
    amount = serializers.IntegerField() 
    currency = serializers.CharField() 


class TransactionSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Transaction 
        fields = '__all__' 

