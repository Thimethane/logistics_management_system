# Generated by Django 5.1.4 on 2025-01-03 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sparepart',
            options={'permissions': [('can_view_sparepart', 'Can view spare part'), ('edit_sparepart', 'Can edit spare part')]},
        ),
    ]