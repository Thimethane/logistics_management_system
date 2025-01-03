from django.db import models
from django.contrib.auth.models import User

class SparePart(models.Model):
    CONDITION_CHOICES = [
        ('serviceable', 'Serviceable'),
        ('unserviceable', 'Unserviceable'),
        ('in-reparation', 'In-Reparation'),
    ]

    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='serviceable')
    location = models.CharField(max_length=100)
    repair_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [
            ("can_view_sparepart", "Can view spare part"),
            ("edit_sparepart", "Can edit spare part"),
        ]

class Component(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in-use', 'In-Use'),
        ('needs-restocking', 'Needs Restocking'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ActionLog(models.Model):
    ACTION_CHOICES = [
        ('add', 'Add'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_affected = models.CharField(max_length=50)
    item_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} performed {self.action_type} on {self.model_affected} ({self.item_id})"
