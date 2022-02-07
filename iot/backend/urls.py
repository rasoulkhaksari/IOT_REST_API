from django.urls import path
from . import views
 
urlpatterns = [ 
    path('device/create/', views.device_create ,name='api_device_create'),
    path('devices/', views.device_list ,name='api_devices'),
]
