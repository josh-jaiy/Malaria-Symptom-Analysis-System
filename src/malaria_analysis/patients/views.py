import os
from django.shortcuts import render, redirect
from .forms import PatientForm, UserRegisterForm
from .models import Patient, Symptom
from django.contrib import messages
from django.http import HttpResponse
from .ml_model import *  # Import the ML logic
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from django.conf import settings
from django.urls import reverse


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to home page
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})


@login_required
def add_patient(request):
    symptoms = Symptom.objects.all()  # Fetch symptoms to display in the form
    
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            # Save the patient object
            patient = form.save(commit=False)  # Don't commit yet
            patient.save()  # Save patient object
            
            # Handle many-to-many relationship for symptoms
            selected_symptoms = request.POST.getlist('symptoms')  # Get list of selected symptoms
            if selected_symptoms:
                patient.symptoms.set(selected_symptoms)  # Link symptoms to patient
            
            messages.success(request, 'Patient data added successfully!')
            return redirect('view_patterns')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PatientForm()
    
    return render(request, 'add_patient.html', {'form': form, 'symptoms': symptoms})


@login_required
def view_patterns(request):
    # Get all patient data
    patients = Patient.objects.all()

    if not patients.exists():
        messages.error(request, 'No patient data available for analysis.')
        return render(request, 'view_patterns.html')

    try:
        # Call the ML model function and get the model and accuracy
        model, accuracy = train_decision_tree(patients)

        # Generate labels and data for the pie chart based on actual patient symptom data
        symptom_labels = [symptom.name for symptom in Symptom.objects.all()]
        
        # Calculate occurrences of each symptom from patient data
        symptom_data = []
        for symptom in Symptom.objects.all():
            symptom_count = sum([1 for patient in patients if symptom in patient.symptoms.all()])
            symptom_data.append(symptom_count)

        context = {
            'accuracy': accuracy,
            'labels': symptom_labels,  # Pie chart labels
            'data': symptom_data,      # Pie chart data
        }
    except Exception as e:
        messages.error(request, f"An error occurred during the analysis: {str(e)}")
        context = {}

    return render(request, 'view_patterns.html', context)


@login_required
def view_exported_result(request):
    # Assume the exported image is saved in the media directory
    plot_image_path = os.path.join(settings.MEDIA_ROOT, 'plots', 'exported_plot.png')

    # Check if the image file exists
    if os.path.exists(plot_image_path):
        plot_image_url = f"{settings.MEDIA_URL}plots/exported_plot.png"  # Use MEDIA_URL for correct URL
    else:
        messages.error(request, "Plot result not found. Please ensure the plot has been generated and exported.")
        plot_image_url = None

    context = {
        'plot_image_url': plot_image_url,
    }

    return render(request, 'view_exported_result.html', context)
