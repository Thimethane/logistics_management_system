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


class ExportUtility:
    @staticmethod
    def export_to_csv(queryset, file_name="exported_data.csv"):
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)
        
        if queryset.model == SparePart:
            writer.writerow(['Name', 'Serial Number', 'Condition', 'Location', 'Created At', 'Updated At'])
            for part in queryset:
                writer.writerow([part.name, part.serial_number, part.condition, part.location, part.created_at, part.updated_at])
        elif queryset.model == Component:
            writer.writerow(['Name', 'Description', 'Quantity', 'Status', 'Classification', 'Created At', 'Updated At'])
            for component in queryset:
                writer.writerow([component.name, component.description, component.quantity, component.status, component.classification, component.created_at, component.updated_at])
        
        output.seek(0)
        return output.getvalue()

    @staticmethod
    def export_to_pdf(queryset, file_name="exported_data.pdf"):
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.pdfgen import canvas

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        if queryset.model == SparePart:
            p.drawString(100, 800, 'Spare Parts List')
            p.setFont("Helvetica", 10)
            y_position = 780
            for part in queryset:
                p.drawString(100, y_position, f"{part.name}, {part.serial_number}, {part.condition}, {part.location}, {part.created_at}, {part.updated_at}")
                y_position -= 20
        elif queryset.model == Component:
            p.drawString(100, 800, 'Component List')
            p.setFont("Helvetica", 10)
            y_position = 780
            for component in queryset:
                p.drawString(100, y_position, f"{component.name}, {component.description}, {component.quantity}, {component.status}, {component.classification}, {component.created_at}, {component.updated_at}")
                y_position -= 20

        p.showPage()
        p.save()

        buffer.seek(0)
        return buffer.read()
