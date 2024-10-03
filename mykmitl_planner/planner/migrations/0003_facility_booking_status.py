# Generated by Django 5.1.1 on 2024-09-30 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0002_alter_facility_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='booking_status',
            field=models.CharField(choices=[('available', 'Available'), ('unavailable', 'Unavailable')], default='available', max_length=20),
        ),
    ]