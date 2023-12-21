from django.contrib import admin
# Register your models here.
from .models import Operations,Table,Permission
admin.site.register(Operations)
admin.site.register(Table)
admin.site.register(Permission)