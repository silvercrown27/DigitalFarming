# Generated by Django 4.2.4 on 2023-09-10 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overviewsite', '0002_remove_agritectusers_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agritectusers',
            name='allocated_space',
            field=models.FloatField(default=5120.0),
        ),
    ]
