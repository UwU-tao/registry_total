# Generated by Django 4.2 on 2023-06-13 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_vehicle_purpose'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicleregistration',
            name='platee',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
