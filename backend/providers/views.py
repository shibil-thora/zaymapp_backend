from django.shortcuts import render
from rest_framework.permissions import BasePermission , IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from services.serializers import ServiceSerializer, ServiceAreaSerializer, ServiceImageSerializer
from services.models import Service, Area, ServiceAreas, ServiceImages 
from rest_framework.exceptions import AuthenticationFailed


# provider permission 
class IsProvider(BasePermission): 
    def has_permission(self, request, view): 
        return request.user.is_provider 
    

class GetServices(APIView): 
    permission_classes = [IsProvider]
    def get(self, request): 
        service_objs = request.user.services.all()
        services = ServiceSerializer(service_objs, many=True).data
        return Response(services) 
    

class AddServiceArea(APIView):
    permission_classes = [IsProvider] 
    def post(self, request):  
        print(request.data) 
        service_id = request.data['service_id'] 
        service = Service.objects.get(id=service_id)
        if request.user.is_premium or service.areas.all().count() < 3: 
            area_obj = Area.objects.get(area_name=request.data['area_name']) 
            area = ServiceAreas.objects.create(area=area_obj, service=service)
            return Response(ServiceAreaSerializer(area).data)
        else: 
            raise AuthenticationFailed("not a premium account")
    

class DeleteServiceArea(APIView):
    permission_classes = [IsProvider] 
    def post(self, request): 
        delete_id = request.data['area_id']['area_data']['id'] 
        print(delete_id)
        print(ServiceAreas.objects.filter(area__id=delete_id).delete())
        return Response(request.data)
    

class DeleteServiceImage(APIView):
    permission_classes = [IsProvider] 
    def post(self, request): 
        delete_id = request.data['image_id'] 
        ServiceImages.objects.filter(id=delete_id).delete()
        return Response(request.data)
    

class AddServiceImage(APIView):
    permission_classes = [IsProvider] 
    def post(self, request):
        print('reached here') 
        service_id = request.data['service_id']
        image = request.FILES['image'] 
        service = Service.objects.get(id=service_id)

        if request.user.is_premium or service.images.all().count() < 3: 
            image_obj = ServiceImages.objects.create(image=image, service=service) 
            image_data = ServiceImageSerializer(image_obj).data
            return Response(image_data) 
        else: 
            raise AuthenticationFailed("not a premium account")