from celery import shared_task  
from django.core.mail import send_mail
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

@shared_task(bind=True)
def send_email_task(self, email, otp): 
    subject = 'ZaymApp verification' 
    message = f'Zaym App Verification Code - {otp}' 
    from_email = settings.EMAIL_HOST_USER 
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
    return 'Email Sent succesfully'