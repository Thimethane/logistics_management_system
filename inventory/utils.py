from io import BytesIO
import csv
from io import StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.db.models import Model

class ExportUtility:
    @staticmethod
    def export_to_csv(queryset, file_name="exported_data.csv"):
        """
        Export data from a queryset to CSV format. Supports dynamic field selection and handles complex relationships
        like ForeignKey and ManyToMany.
        """
        if not queryset or not isinstance(queryset.model, Model):
            raise ValueError("Invalid queryset provided")

        # Create in-memory string buffer for CSV
        output = StringIO()
        writer = csv.writer(output)

        # Dynamically extract model field names for headers
        model = queryset.model
        headers = [field.name for field in model._meta.fields if field.name != 'id']
        
        # Add headers to the CSV
        writer.writerow(headers)

        # Writing rows from the queryset
        for obj in queryset:
            row = []
            for field in headers:
                value = getattr(obj, field)
                
                # Handle ForeignKey and ManyToMany relationships by getting human-readable representations
                if hasattr(value, '__str__'):  # If it's a related object
                    value = str(value)
                elif isinstance(value, (list, set)):  # For ManyToMany fields
                    value = ', '.join([str(v) for v in value])

                row.append(value)

            writer.writerow(row)

        # Get the CSV data as string and return it
        output.seek(0)
        return output.getvalue()
    
    @staticmethod
    def download_csv(queryset, file_name="exported_data.csv"):
        csv_data = ExportUtility.export_to_csv(queryset)
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response

    @staticmethod
    def export_to_pdf(queryset, file_name="exported_data.pdf"):
        """
        Export data from a queryset to PDF format. Supports dynamic field selection and handles complex relationships
        like ForeignKey and ManyToMany.
        """
        # Validate queryset
        if queryset is None or not queryset.exists() or not isinstance(queryset.model, Model):
            raise ValueError("Invalid or empty queryset provided")

        # Create in-memory buffer for PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        # Get the model and field names dynamically
        model = queryset.model
        fields = [field.name for field in model._meta.fields if field.name != 'id']
        
        # Drawing the title at the top of the page
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 800, f"{model._meta.verbose_name.title()} List")

        # Setting font for the table
        p.setFont("Helvetica", 10)
        
        # Header Row - adjust for dynamic fields
        y_position = 780
        for i, field in enumerate(fields):
            p.drawString(100 + (i * 100), y_position, field.capitalize())

        y_position -= 20

        # Writing rows - dynamically handling different field types
        for obj in queryset:
            row = []
            for field in fields:
                value = getattr(obj, field)

                # Handle ForeignKey and ManyToMany relationships by getting human-readable representations
                if hasattr(value, '__str__'):  # If it's a related object (ForeignKey)
                    value = str(value)
                elif isinstance(value, (list, set)):  # For ManyToMany fields
                    value = ', '.join([str(v) for v in value])

                row.append(value)

            # Write the row data to the PDF
            for i, cell_value in enumerate(row):
                p.drawString(100 + (i * 100), y_position, str(cell_value))
            y_position -= 20  # Move to the next row

            # Add a page break if the content exceeds the page length
            if y_position < 100:
                p.showPage()
                p.setFont("Helvetica", 10)
                y_position = 780  # Reset the y_position for the new page

        # Finalizing the PDF
        p.showPage()
        p.save()

        # Return the PDF data as bytes
        buffer.seek(0)
        return buffer.read()
    
    @staticmethod
    def download_pdf(queryset, file_name="exported_data.pdf"):
        try:
            pdf_data = ExportUtility.export_to_pdf(queryset)
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
        except Exception as e:
            return HttpResponse(f"Export Error: {str(e)}", status=400)
