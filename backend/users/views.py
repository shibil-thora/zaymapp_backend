from django.shortcuts import render 
from rest_framework.response import Response 
from rest_framework.views import APIView  
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import authenticate 
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer , NotificationSerializer
from .models import MyUsers as User 
from django.core.validators import EmailValidator
from services.serializers import AreaSerializer, ServiceSerializer, DisplayServiceSerializer
from services.models import Area, UserArea, Service
from django.contrib.auth.models import AnonymousUser 
import random
from django.core.cache import cache
from datetime import datetime, timedelta 
from .models import Notification 
from django.core.mail import send_mail 
from django.conf import settings


class UserLoginView(APIView): 
    def post(self, request):
        username = request.data['username']
        password = request.data['password'] 
        user = authenticate(username=username, password=password) 
        if user is None: 
            raise AuthenticationFailed('invalid credentials') 
        
        refresh = RefreshToken.for_user(user) 
        access = refresh.access_token 
        user_data = UserSerializer(user) 
        user_dict = user_data.data 
        area = None 
        try: 
            area_obj = user.area.area 
            area = AreaSerializer(area_obj).data
        except: 
            pass

        response_data = {
            'refresh': str(refresh),
            'access': str(access), 
            'user': {
                'username': user_dict['username'],
                'email': user_dict['email'], 
                'is_authenticated': user_dict['is_authenticated'],
                'is_active': user_dict['is_active'],  
                'is_superuser': user_dict['is_superuser'],
                'is_provider': user_dict['is_provider'],
                'is_premium': user_dict['is_premium'], 
                'area': area, 
                'pro_pic': user_dict['profile_picture']
            }
        }
    
        return Response(response_data) 
    

class UserStatusView(APIView): 
    def get(self, request): 
        user = request.user
        user_data = UserSerializer(user) 
        user_dict = user_data.data
        area = None 
        try: 
            area_obj = user.area.area 
            area = AreaSerializer(area_obj).data
        except: 
            pass
        response_data = None
        if isinstance(user, AnonymousUser): 
            response_data = {
                'user': {
                    'username': None,
                    'email': None, 
                    'is_authenticated': None,
                    'is_active': None,  
                    'is_superuser': None,
                    'is_premium': None, 
                    'is_provider': None,
                    'area': area,
                    'pro_pic': None
                }   
            }
        else: 
            response_data = {
                'user': {
                    'username': user_dict['username'],
                    'email': user_dict['email'], 
                    'is_authenticated': user_dict['is_authenticated'],
                    'is_active': user_dict['is_active'],  
                    'is_superuser': user_dict['is_superuser'],
                    'is_provider': user_dict['is_provider'], 
                    'is_premium': user_dict['is_premium'], 
                    'area': area,
                    'pro_pic': user_dict['profile_picture']
                }
            }
        return Response(response_data) 
    

class UserSignUpView(APIView): 
    def post(self, request): 
        username = request.data.get('username')
        email = request.data.get('email')
        pass1 = request.data.get('pass1')
        pass2 = request.data.get('pass2')
        print(username, email, pass1, pass2)

        if not pass1 == pass2: 
            raise AuthenticationFailed('passwords do not match!') 
        
        if User.objects.filter(username=username): 
            raise AuthenticationFailed('username already exists') 
        
        if User.objects.filter(email=email):
            raise AuthenticationFailed('email already exists') 
        
        if len(username.strip()) < 4:  
            raise AuthenticationFailed('username is short')
        
        if str(username).isdigit(): 
            raise AuthenticationFailed('invalid username') 
        
        try: 
            EmailValidator()(email)
        except: 
            raise AuthenticationFailed('Enter a valid email') 
        
        if len(pass1.strip()) < 5: 
            raise AuthenticationFailed('short password') 
        
        #User.objects.create_user(username=username, email=email, password=pass1)
        
        return Response({'message': 'user Created'}) 
    

class UserRegisterView(APIView): 
    def post(self, request): 
        username = request.data.get('username')
        email = request.data.get('email')
        pass1 = request.data.get('pass1')
        pass2 = request.data.get('pass2')
        print(username, email, pass1, pass2)
        User.objects.create_user(username=username, email=email, password=pass1)
        return Response({'message': 'user Created'}) 
    

class UserListView(APIView): 
    permission_classes = [IsAdminUser]
    def get(self, request): 
        user_objs = User.objects.all()
        user_objs = user_objs.exclude(is_superuser=True)
        user_set = UserSerializer(user_objs, many=True)
        return Response({"users": user_set.data})
    

class ToggleBlockView(APIView): 
    permission_classes = [IsAdminUser]
    def post(self, request): 
        user_id = request.data['id'] 
        user = User.objects.get(id=user_id) 
        if user.is_active: 
            user.is_active = False
            user.save()
        else:
            user.is_active = True 
            user.save()
        return Response({'id': user_id, 'status': user.is_active})
    

class EditUserArea(APIView): 
    permission_classes = [IsAuthenticated]
    def post(self, request): 
        user = request.user 
        new_area = Area.objects.get(id=request.data['id'])
        try:
            area = user.area 
            area.area = new_area 
            area.save()
            return Response(AreaSerializer(new_area).data)
        except: 
            UserArea.objects.create(user=request.user, area=new_area)
            return Response(AreaSerializer(new_area).data) 
        

class UpdateProfilePic(APIView): 
    permission_classes = [IsAuthenticated] 
    def post(self, request): 
        user = request.user 
        user.profile_picture = request.FILES['image']
        user.save()
        return Response(user.profile_picture.url)
    

class GetDisplayServiceList(APIView): 
    def get(self, request): 
        service_objs = Service.objects.all().filter(permit=True)
        response_data = DisplayServiceSerializer(service_objs, many=True).data
        return Response(response_data) 
    

class SendOTP(APIView): 
    def post(self, request): 
        def send_email_task(email, otp): 
            subject = 'ZaymApp verification' 
            message = f'Zaym App Verification Code - {otp}' 
            from_email = settings.EMAIL_HOST_USER 
            recipient_list = [email]
            send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
            return 'Email Sent succesfully' 
        
        email = request.data['email'] 
        otp = random.randint(100000, 999999)
        send_email_task(email=email, otp=otp)  
        cache.set(email, (otp, datetime.now()))
        return Response('success')  
    

class VerifyOTP(APIView): 
    def post(self, request):  

        def otp_is_valid(otp, sent_otp, sent_time): 
            OTP_DURATION = 65  #seconds
            if not otp == sent_otp: 
                return False
            time_diff = datetime.now() - sent_time 
            return time_diff.total_seconds() <= OTP_DURATION

        email = request.data['email'] 
        otp = request.data['otp']
        sent_otp, sent_time = cache.get(email) 
        sent_otp = str(sent_otp)  
        if not otp_is_valid(otp, sent_otp, sent_time): 
            raise AuthenticationFailed('Wrong OTP!') 
        response_data = {
            'message': 'otp verification successful'
        }
        return Response(response_data)
    

class ChangePassword(APIView): 
    permission_classes = [IsAuthenticated] 
    def post(self, request): 
        user = request.user 
        is_auth = authenticate(username=user.username, password=request.data['current_pass'])
        new_password = request.data['new_pass']

        if is_auth is None: 
            raise AuthenticationFailed('current password is wrong!') 
        
        if len(new_password.strip()) < 5: 
            raise AuthenticationFailed('short password')
    
        user.set_password(new_password) 
        user.save()
        return Response('ok') 
    

class GetNotifications(APIView): 
    permission_classes = [IsAuthenticated] 
    def get(self, request):  
        user = request.user 
        notify_ojbs = user.notifications.all().order_by('-id') 
        notify_data = NotificationSerializer(notify_ojbs, many=True).data
        return Response(notify_data)
    

class SeeNotifications(APIView): 
    permission_classes = [IsAuthenticated] 
    def post(self, request):  
        delete_id = request.data['noti_id']
        Notification.objects.filter(id=delete_id).delete()
        return Response('deleted') 
    

class UserGroupListView(APIView): 
    permission_classes = [IsAdminUser] 
    def get(self, request): 
        users = User.objects.filter(
            is_provider=False, 
            is_superuser=False, 
            is_premium=False, 
        ) 
        providers = User.objects.filter(is_provider=True)
        premium = User.objects.filter(is_premium=True) 
        admin = User.objects.filter(is_superuser=True) 

        response_data = [
            {'name': 'users', 'value': users.count()},
            {'name': 'providers', 'value': providers.count()}, 
            {'name': 'premium users', 'value': premium.count()}, 
            {'name': 'admins', 'value': admin.count()}, 
        ]

        return Response(response_data)