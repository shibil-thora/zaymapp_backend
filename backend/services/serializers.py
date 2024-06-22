from rest_framework import serializers 
from . models import Area, Service, ServiceType , UserArea, ServiceAreas, ServiceImages
from . models import KnockedUsers
from users.serializers import UserSerializer


class AreaSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Area 
        fields = '__all__'


class UserAreaSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = UserArea 
        fields = '__all__' 


class ServiceAreaSerializer(serializers.ModelSerializer): 
    area_data = AreaSerializer(read_only=True)
    class Meta: 
        model = ServiceAreas 
        fields = [
            'area_data'
        ]


class ServiceImageSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = ServiceImages 
        fields = ['id', 'service', 'image']


class KnockedUserSerializer(serializers.ModelSerializer): 
    user_data = UserSerializer(read_only=True)
    class Meta: 
        model = KnockedUsers 
        fields = [
            'id', 
            'user_data'
        ]


class ServiceSerializer(serializers.ModelSerializer): 
    get_user = UserSerializer(read_only=True)
    get_areas = ServiceAreaSerializer(many=True)  
    get_knocks = KnockedUserSerializer(many=True)
    class Meta: 
        model = Service 
        fields = [
            'id',
            'user', 
            'business_name', 
            'service_type', 
            'available', 
            'permit', 
            'description', 
            'cover_image', 
            'knock_count',
            'get_user', 
            'get_areas', 
            'get_images',
            'get_knocks', 
        ] 


class DisplayServiceSerializer(serializers.ModelSerializer): 
    get_user = UserSerializer(read_only=True) 
    get_areas = ServiceAreaSerializer(many=True)
    get_knocks = KnockedUserSerializer(many=True) 

    class Meta: 
        model = Service 
        fields = [
            'id', 
            'business_name', 
            'service_type', 
            'cover_image', 
            'description', 
            'get_user', 
            'get_areas',
            'get_images', 
            'get_knocks', 
        ]


class ServiceTypeSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = ServiceType 
        fields = '__all__'
    

    