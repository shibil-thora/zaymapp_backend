from django.urls import path 
from . import views

urlpatterns = [
    path('get_services/', views.GetServices.as_view()), 
    path('add_service_area/', views.AddServiceArea.as_view()), 
    path('add_service_image/', views.AddServiceImage.as_view()), 
    path('delete_service_area/', views.DeleteServiceArea.as_view()), 
    path('delete_service_image/', views.DeleteServiceImage.as_view()), 
]
