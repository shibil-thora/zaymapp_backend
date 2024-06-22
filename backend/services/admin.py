from django.contrib import admin
from .models import Area, Service, ServiceAreas, ServiceType, UserArea
from .models import ServiceImages, KnockedUsers


admin.site.register(Area)
admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(ServiceAreas)
admin.site.register(UserArea) 
admin.site.register(ServiceImages)
admin.site.register(KnockedUsers)