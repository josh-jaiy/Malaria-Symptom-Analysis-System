from django.test import TestCase

# Create your tests here.
from .models import Patient

class PatientModelTest(TestCase):
    def setUp(self):
        Patient.objects.create(age=25, gender='Male', malaria_type='Plasmodium falciparum')

    def test_patient_age(self):
        patient = Patient.objects.get(age=25)
        self.assertEqual(patient.age, 25)
