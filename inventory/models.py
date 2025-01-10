from django.db import models
from django.contrib.auth.models import User
from django.db import transaction

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
    repair_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number}) - {self.get_condition_display()}"

    def is_serviceable(self):
        """Check if the spare part is serviceable."""
        return self.condition == 'serviceable'

    @staticmethod
    def serviceable_parts():
        """Retrieve all serviceable spare parts."""
        return SparePart.objects.filter(condition='serviceable')

    @staticmethod
    def unserviceable_parts():
        """Retrieve all unserviceable spare parts."""
        return SparePart.objects.filter(condition='unserviceable')

    class Meta:
        permissions = [
            ("can_view_sparepart", "Can view spare part"),
            ("edit_sparepart", "Can edit spare part"),
        ]
        
    @transaction.atomic
    def move_to_condition(self, new_condition):
        """Move a spare part to a new condition category."""
        if new_condition not in dict(self.CONDITION_CHOICES):
            raise ValueError(f"Invalid condition: {new_condition}")
        old_condition = self.condition
        self.condition = new_condition
        self.save()
        # Log the action
        ActionLog.objects.create(
            user=None,  # Replace with current user in view
            action_type='edit',
            model_affected='SparePart',
            item_id=self.id,
        )
        return f"Moved {self.name} from {old_condition} to {new_condition}"


class Component(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in-use', 'In-Use'),
        ('needs-restocking', 'Needs Restocking'),
    ]

    CLASSIFICATION_CHOICES = [
        ('serviceable', 'Serviceable'),
        ('non-serviceable', 'Non-Serviceable'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    classification = models.CharField(max_length=20, choices=CLASSIFICATION_CHOICES, default='serviceable')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_status_display()} - {self.get_classification_display()}"

    def is_available(self):
        """Check if the component is available."""
        return self.status == 'available'

    @staticmethod
    def available_components():
        """Retrieve all available components."""
        return Component.objects.filter(status='available')

    @staticmethod
    def serviceable_components():
        """Retrieve all serviceable components."""
        return Component.objects.filter(classification='serviceable')

    @staticmethod
    def non_serviceable_components():
        """Retrieve all non-serviceable components."""
        return Component.objects.filter(classification='non-serviceable')

    class Meta:
        permissions = [
            ("can_view_component", "Can view component"),
            ("edit_component", "Can edit component"),
        ]
        
    @transaction.atomic
    def move_to_status(self, new_status):
        """Move a component to a new status category."""
        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError(f"Invalid status: {new_status}")
        old_status = self.status
        self.status = new_status
        self.save()
        ActionLog.objects.create(
            user=None,  # Replace with current user in view
            action_type='edit',
            model_affected='Component',
            item_id=self.id,
        )
        return f"Moved {self.name} from {old_status} to {new_status}"


class ActionLog(models.Model):
    ACTION_CHOICES = [
        ('add', 'Add'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
        ('export', 'Export'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_affected = models.CharField(max_length=50)
    item_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} performed {self.get_action_type_display()} on {self.model_affected} ({self.item_id})"
    
    @staticmethod
    def get_logs_by_user(user):
        """Retrieve logs for a specific user."""
        return ActionLog.objects.filter(user=user).order_by('-timestamp')

    @staticmethod
    def get_logs_for_model(model_name):
        """Retrieve logs for a specific model."""
        return ActionLog.objects.filter(model_affected=model_name).order_by('-timestamp')
