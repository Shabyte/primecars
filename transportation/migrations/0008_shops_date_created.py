# Generated by Django 5.0.4 on 2024-10-10 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0007_shops_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='shops',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]