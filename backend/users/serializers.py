from rest_framework import serializers 
from . models import MyUsers , Notification


class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = MyUsers 
        fields = [
            'id', 
            'username', 
            'email', 
            'is_authenticated', 
            'is_active', 
            'is_premium',
            'is_superuser', 
            'profile_picture', 
            'is_provider', 
        ] 


class NotificationSerializer(serializers.ModelSerializer): 
    informer_data = UserSerializer(read_only=True) 
    class Meta: 
        model = Notification 
        fields = [
            'id', 
            'informer', 
            'receiver', 
            'message', 
            'date', 
            'informer_data'
        ]