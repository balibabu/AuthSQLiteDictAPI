from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Operations

@receiver(post_migrate)
def create_default_operations(sender, **kwargs):
    if sender.name == 'sqlapi': 
        default_operations = [
            {"opTitle": "__all__"},
            {"opTitle": "read"},
            {"opTitle": "insert"},
            {"opTitle": "override"},
            {"opTitle": "delete"},
        ]

        for op_data in default_operations:
            Operations.objects.get_or_create(**op_data)
