from django.db import models
from django.contrib.auth.models import User

class Table(models.Model):
    creator=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    table_name=models.CharField(max_length=255)

class Operations(models.Model):
    opTitle=models.CharField(max_length=20)

class Permission(models.Model):
    operation=models.ForeignKey(Operations,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    table=models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    

    
