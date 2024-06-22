from django.urls import path 
from . import views

urlpatterns = [
    path('get_areas/', views.GetAreas.as_view()), 
    path('set_scripts/', views.SetService.as_view()), 
    path('create/', views.CreateService.as_view()), 
    path('edit/', views.EditService.as_view()), 
    path('get_services/', views.GetServices.as_view()), 
    path('allow_permit/', views.AllowPermit.as_view()), 
    path('get_types/', views.GetTypes.as_view()), 
    path('edit_types/', views.EditServiceType.as_view()), 
    path('add_types/', views.AddServiceType.as_view()), 
    path('hide_types/', views.HideTypes.as_view()), 
    path('unhide_types/', views.UnHideTypes.as_view()), 
    path('ban_area/', views.BanAreas.as_view()), 
    path('permit_area/', views.PermitAreas.as_view()), 
    path('knock_service/', views.KnockService.as_view()),  
]
