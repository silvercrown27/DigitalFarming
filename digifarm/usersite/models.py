import uuid

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from overviewsite.models import AgritectUsers


class PlantDatabase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PlantDiseases(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    disease_name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    plantid = models.ForeignKey(PlantDatabase, on_delete=models.CASCADE)
    causes = models.TextField()
    prevention_measures = models.TextField()
    cures = models.TextField()

    def __str__(self):
        return self.disease_name


class PlantsAnalyzed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(AgritectUsers, on_delete=models.CASCADE)
    plant_name = models.CharField(max_length=255)
    STATUS_CHOICES = (
        ('Healthy', 'Healthy'),
        ('Sick', 'Sick'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    disease_name = models.CharField(max_length=255)

    DISEASE_TYPE_CHOICES = (
        ('None', 'None'),
        ('Deficiency', 'Deficiency'),
        ('Illness/Infection', 'Illness/Infection'),
    )
    disease_type = models.CharField(max_length=20, choices=DISEASE_TYPE_CHOICES)

    image_path = models.ImageField(upload_to='analyzed_images/')
    date_detected = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.firstname}'s Analysis of {self.plant_name} ({self.status})"


class Deficiency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    nutrient_name = models.CharField(max_length=255, help_text="Name of the nutrient causing deficiency")
    symptoms = models.TextField(help_text="Symptoms of the deficiency")
    recommended_actions = models.TextField(help_text="Recommended actions to address the deficiency")
    image_path = models.ImageField(upload_to='deficiency_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.plant_name} Nutrient Deficiency: {self.nutrient_name}"


class Drives(models.Model):
    id = models.CharField(max_length=15, primary_key=True, editable=False, unique=True, blank=False, null=False)
    drive_name = models.CharField(max_length=25, null=False, blank=False, editable=True)
    drive_user = models.ForeignKey(AgritectUsers, on_delete=models.CASCADE)
    capacity = models.IntegerField(validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4().hex[:15]).upper()
        super().save(*args, **kwargs)


class Folders(models.Model):
    id = models.CharField(max_length=15, primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    path_regex = RegexValidator(
        regex=r'^[/\w.@+-]*(?:[/\w@+-]+)*$',
        message='Path must start with a slash, and can contain letters, digits,'
                'hyphens, underscores, dots, at signs, plus signs, and slashes.')
    path = models.CharField(validators=[path_regex], max_length=1000, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now_add=True)
    drive_id = models.ForeignKey(Drives, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4().hex[:15]).upper()
        super().save(*args, **kwargs)


class Files(models.Model):
    id = models.CharField(max_length=15, primary_key=True, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    path_regex = RegexValidator(
        regex=r'^[/\w.@+-]*(?:[/\w@+-]+)*$',
        message='Path must start with a slash, and can contain letters, digits,'
                'hyphens, underscores, dots, at signs, plus signs, and slashes.')
    path = models.CharField(validators=[path_regex], max_length=1000, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    file_ext = models.CharField(max_length=100, blank=True)
    file_size = models.IntegerField(blank=True, null=True)
    folder_id = models.ForeignKey(Folders, on_delete=models.CASCADE)
    drive_id = models.ForeignKey(Drives, on_delete=models.CASCADE, default=1)

    def clean(self):
        max_file_size = self.drive_id.capacity
        if self.file_size and self.file_size > max_file_size:
            raise ValidationError(f'The file size ({self.file_size}) exceeds the maximum capacity of the drive ({max_file_size}).')

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4().hex[:15]).upper()
        super().save(*args, **kwargs)