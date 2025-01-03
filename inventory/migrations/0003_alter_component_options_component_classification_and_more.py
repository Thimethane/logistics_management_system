# Generated by Django 5.1.4 on 2025-01-03 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_sparepart_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='component',
            options={'permissions': [('can_view_component', 'Can view component'), ('edit_component', 'Can edit component')]},
        ),
        migrations.AddField(
            model_name='component',
            name='classification',
            field=models.CharField(choices=[('serviceable', 'Serviceable'), ('non-serviceable', 'Non-Serviceable')], default='serviceable', max_length=20),
        ),
        migrations.AlterField(
            model_name='actionlog',
            name='action_type',
            field=models.CharField(choices=[('add', 'Add'), ('edit', 'Edit'), ('delete', 'Delete'), ('export', 'Export')], max_length=20),
        ),
        migrations.AlterField(
            model_name='component',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='sparepart',
            name='repair_history',
            field=models.TextField(blank=True, null=True),
        ),
    ]