from dataclasses import fields
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import IOTdevice

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

# class IOTdeviceSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = IOTdevice
#         fields = ['url','device_id','customer_id','reading','timestamp']

class IOTdeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IOTdevice
        fields = '__all__'


