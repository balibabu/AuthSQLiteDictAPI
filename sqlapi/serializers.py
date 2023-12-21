from rest_framework import serializers
from .models import Table, Permission, Operations

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class OperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operations
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

