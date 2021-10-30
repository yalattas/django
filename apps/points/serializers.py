from rest_framework import serializers
from .models import *

class FirstApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['id']

class AddNewEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'