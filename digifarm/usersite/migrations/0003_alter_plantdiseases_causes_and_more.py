# Generated by Django 4.2.4 on 2023-09-11 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usersite', '0002_deficiency_plantdiseases_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantdiseases',
            name='causes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='plantdiseases',
            name='disease_name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='plantdiseases',
            name='plantid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usersite.plantdatabase'),
        ),
    ]
