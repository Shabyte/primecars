# Generated by Django 5.0.4 on 2024-10-24 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0034_rented_cars_total_hrs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver_shop',
            name='drivers_rate',
            field=models.IntegerField(verbose_name='Driver Hourly Rate'),
        ),
    ]