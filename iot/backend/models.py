from django.contrib.auth.models import User
from django.db import models

class IOTdevice(models.Model):
    timestamp=models.DateTimeField() 
    reading=models.FloatField(null=False)
    device_id=models.CharField(max_length=36,null=False)
    customer_id=models.CharField(max_length=36,null=False)

    class Meta:
        db_table = 'IOTdevice'

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    customer_id=models.CharField(max_length=36,null=False)