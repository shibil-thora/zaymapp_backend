from __future__ import absolute_import, unicode_literals 
import os 

from celery import Celery 
from django.conf import settings  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend') 
app.conf.enable_utc = False 

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY') 

#Celery Beat Settings  
 
app.autodiscover_tasks() 

@app.task(bind=True)
def debug_task(self): 
    print(f'Request: {self.request!r}') 

# enter the command below on the command line while development phase
# celery -A backend.celery worker --pool=solo -l info 





# https://youtu.be/EfWa6KH8nVI?si=vEo8-UXQ4ETjmrQO