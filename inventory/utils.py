# inventory/utils.py

import csv
from io import StringIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ExportUtility:

    @staticmethod
    def export_to_csv(items, filename="export.csv"):
        """
        Convert data to CSV format and prepare for download.
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Description', 'Classification', 'Location', 'Serial Number'])
        
        for item in items:
            writer.writerow([item.name, item.description, item.classification, item.location, item.serial_number])
        
        return response

    @staticmethod
    def export_to_pdf(items, filename="export.pdf"):
        """
        Export data to a PDF format and prepare for download.
        """
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        c = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # Set up title and column headers
        c.setFont("Helvetica-Bold", 12)
        c.drawString(200, height - 40, "Exported Data Report")
        c.setFont("Helvetica", 10)

        # Define column positions
        y_position = height - 60
        c.drawString(30, y_position, "Name")
        c.drawString(150, y_position, "Description")
        c.drawString(300, y_position, "Classification")
        c.drawString(450, y_position, "Location")
        c.drawString(600, y_position, "Serial Number")

        # Add data rows
        for item in items:
            y_position -= 20
            c.drawString(30, y_position, item.name)
            c.drawString(150, y_position, item.description)
            c.drawString(300, y_position, item.classification)
            c.drawString(450, y_position, item.location)
            c.drawString(600, y_position, str(item.serial_number))

            if y_position <= 60:  # Add a new page if space is exhausted
                c.showPage()
                c.setFont("Helvetica", 10)
                y_position = height - 40  # Reset y_position for new page

        c.save()
        return response
