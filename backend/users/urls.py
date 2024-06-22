from django.urls import path 
from . import views

urlpatterns = [
    path('login/', views.UserLoginView().as_view()), 
    path('signup/', views.UserSignUpView().as_view()), 
    path('register/', views.UserRegisterView().as_view()), 
    path('user_status/', views.UserStatusView.as_view()), 
    path('zaymadmin/users_list/', views.UserListView.as_view()), 
    path('zaymadmin/user_group_list/', views.UserGroupListView.as_view()), 
    path('zaymadmin/toggleblock/', views.ToggleBlockView.as_view()), 
    path('edit_area/', views.EditUserArea.as_view()),
    path('update_profile_pic/', views.UpdateProfilePic.as_view()), 
    path('display_service_list/', views.GetDisplayServiceList.as_view()), 
    path('send_otp', views.SendOTP.as_view()), 
    path('verify_otp', views.VerifyOTP.as_view()), 
    path('change_password/', views.ChangePassword.as_view()), 
    path('get_notifications/', views.GetNotifications.as_view()),
    path('see_notification/', views.SeeNotifications.as_view()),
]
