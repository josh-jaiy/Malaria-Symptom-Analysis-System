from django import forms
from .models import Patient, Symptom
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['age', 'gender', 'malaria_type', 'symptoms']
        widgets = {
            'symptoms': forms.CheckboxSelectMultiple(),
        }




class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
