# Generated by Django 4.2.4 on 2023-09-11 22:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('usersite', '0004_alter_plantdiseases_causes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantsanalyzed',
            name='date_detected',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]