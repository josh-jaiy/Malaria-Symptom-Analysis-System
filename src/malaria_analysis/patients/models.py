from django.db import models
from django.contrib.auth.models import User

class Symptom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()  # Add this field

    def __str__(self):
        return self.name


class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    MALARIA_TYPES = [
        ('P. falciparum', 'Plasmodium falciparum'),
        ('P. vivax', 'Plasmodium vivax'),
        ('P. ovale', 'Plasmodium ovale'),
        ('P. malariae', 'Plasmodium malariae'),
    ]

    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    malaria_type = models.CharField(max_length=50, choices=MALARIA_TYPES)
    symptoms = models.ManyToManyField(Symptom)

    def __str__(self):
        return f"Patient {self.id} - {self.malaria_type}"
