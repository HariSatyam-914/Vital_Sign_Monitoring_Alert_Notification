import pdfplumber
import re
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import RegistrationForm
from .models import Patient
from .forms import PatientReportForm
from .utils import extract_patient_data  # Import the extraction function
from .models import PatientDetails  # Import your model
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from .models import PatientInfo
import csv
from django.http import HttpResponse
import logging
import numpy as np
import os
import pandas as pd
import joblib
import xgboost as xgb
import fitz  # PyMuPDF for PDF extraction
from .forms import PatientForm 
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def home(request):
    #check the logged users
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #authenticate user
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'You are now logged in')
            # then we have to redirect to the page
            return redirect('home')
        else:
            messages.error(request,'Invalid username or password')
            return redirect('home')
    else:
        return render(request,'home.html',{})

# def login_view(request):
#     pass

def logout_view(request):
    logout(request)
    messages.success(request,'You are now logged out')
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You are successfully registered and welcome to our site')
            return redirect('home')
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form':form})


def dashboard_view(request):
    return render(request,'dashboard.html',{})


def patient_info(request):
    patients = Patient.objects.all()  # Fetch all patient records
    return render(request, 'patient_info.html', {'patients': patients})


def patient_details(request):
    patients = Patient.objects.all()  # Fetch all patients from the database
    return render(request, 'patient_details.html', {'patients': patients})

def add_patient(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        age = request.POST['age']
        gender = request.POST['gender']
        phone_number = request.POST['phone_number']
        body_temperature = request.POST['body_temperature']
        spo2 = request.POST['spo2']
        heart_rate = request.POST['heart_rate']
        respiration_rate = request.POST['respiration_rate']
        blood_pressure_systolic = request.POST['blood_pressure_systolic']
        blood_pressure_diastolic = request.POST['blood_pressure_diastolic']

        # Save to database
        patient = Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            phone_number=phone_number,
            body_temperature=body_temperature,
            spo2=spo2,
            heart_rate=heart_rate,
            respiration_rate=respiration_rate,
            blood_pressure_systolic=blood_pressure_systolic,
            blood_pressure_diastolic=blood_pressure_diastolic
        )
        patient.save()  # ✅ Ensure saving

        return redirect('patient_details')  

    return render(request, 'patient_details.html')


def predict_health(request, patient_id=None):
    if patient_id:
        patient = get_object_or_404(Patient, id=patient_id)
        # Process prediction for this specific patient
        # Example: Run ML model on patient's data
        health_status = "Healthy"  # Replace with your ML model's output

        return render(request, 'predict_health.html', {'patient': patient, 'health_status': health_status})

    patients = Patient.objects.all()
    return render(request, 'predict_health.html', {'patients': patients})

def upload_report(request):
    return render(request, 'upload_report.html')

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return redirect('patient_details')

def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        patient.first_name = request.POST['first_name']
        patient.last_name = request.POST['last_name']
        patient.age = request.POST['age']
        patient.gender = request.POST['gender']
        patient.phone_number = request.POST['phone_number']
        patient.body_temperature = request.POST['body_temperature']
        patient.spo2 = request.POST['spo2']
        patient.heart_rate = request.POST['heart_rate']
        patient.respiration_rate = request.POST['respiration_rate']
        patient.blood_pressure_systolic = request.POST['blood_pressure_systolic']
        patient.blood_pressure_diastolic = request.POST['blood_pressure_diastolic']
        patient.save()
        return redirect('patient_details')  # Redirect to patient list

    return render(request, 'edit_patient.html', {'patient': patient})


def extract_patient_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    # Extracting Patient Info using Regular Expressions
    data = {
        "patient_name": re.search(r"Patient Name:\s*([\w\s]+)", text).group(1) if re.search(r"Patient Name:\s*([\w\s]+)", text) else "Unknown",
        "age": int(re.search(r"Age:\s*(\d+)", text).group(1)) if re.search(r"Age:\s*(\d+)", text) else 0,
        "gender": re.search(r"Gender:\s*(\w+)", text).group(1) if re.search(r"Gender:\s*(\w+)", text) else "Unknown",
        "phone_number": re.search(r"Phone:\s*([\d-]+)", text).group(1) if re.search(r"Phone:\s*([\d-]+)", text) else "Unknown",
        "body_temperature": float(re.search(r"Temperature:\s*([\d.]+)", text).group(1)) if re.search(r"Temperature:\s*([\d.]+)", text) else 0.0,
        "spo2": float(re.search(r"SpO2:\s*([\d.]+)", text).group(1)) if re.search(r"SpO2:\s*([\d.]+)", text) else 0.0,
        "heart_rate": int(re.search(r"Heart Rate:\s*(\d+)", text).group(1)) if re.search(r"Heart Rate:\s*(\d+)", text) else 0,
        "respiration_rate": int(re.search(r"Respiration Rate:\s*(\d+)", text).group(1)) if re.search(r"Respiration Rate:\s*(\d+)", text) else 0,
        "blood_pressure_systolic": int(re.search(r"BP Systolic:\s*(\d+)", text).group(1)) if re.search(r"BP Systolic:\s*(\d+)", text) else 0,
        "blood_pressure_diastolic": int(re.search(r"BP Diastolic:\s*(\d+)", text).group(1)) if re.search(r"BP Diastolic:\s*(\d+)", text) else 0,
    }

    return data

def upload_medical_report(request):
    extracted_data = {}

    if request.method == "POST" and "medical_report" in request.FILES:
        pdf_file = request.FILES["medical_report"]
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"

        # Dummy extraction logic (replace with actual extraction code)
        extracted_data = {
            "patient_name": "John Doe",  # Extracted from text
            "age": 32,
            "gender": "Male",
            "phone_number": "9876543210",
            "body_temperature": "37.2",
            "spo2": "98",
            "heart_rate": "75",
            "respiration_rate": "16",
            "blood_pressure_systolic": "120",
            "blood_pressure_diastolic": "80",
        }

        request.session["extracted_data"] = extracted_data  # Store in session

    return render(request, "upload_medical_report.html", {"extracted_data": extracted_data})

def add_extracted_data(request):
    extracted_data = request.session.get("extracted_data")

    if extracted_data:
        PatientDetails.objects.create(
            patient_name=extracted_data["patient_name"],
            age=extracted_data["age"],
            gender=extracted_data["gender"],
            phone_number=extracted_data["phone_number"],
            body_temperature=extracted_data["body_temperature"],
            spo2=extracted_data["spo2"],
            heart_rate=extracted_data["heart_rate"],
            respiration_rate=extracted_data["respiration_rate"],
            blood_pressure_systolic=extracted_data["blood_pressure_systolic"],
            blood_pressure_diastolic=extracted_data["blood_pressure_diastolic"],
        )
        del request.session["extracted_data"]  # Clear session after saving

    return redirect("patient_details")  # Redirect to patient details page
logger = logging.getLogger(__name__)

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patient_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Age', 'Gender', 'Phone Number', 
                     'Body Temperature', 'SpO2', 'Heart Rate', 'Respiration Rate', 
                     'BP Systolic', 'BP Diastolic'])

    patients = Patient.objects.all()  # ✅ Using the correct model

    for patient in patients:
        writer.writerow([
            patient.first_name, patient.last_name, patient.age, patient.gender,
            patient.phone_number, patient.body_temperature, patient.spo2, 
            patient.heart_rate, patient.respiration_rate, 
            patient.blood_pressure_systolic, patient.blood_pressure_diastolic
        ])

    return response


# Load the trained model and scalers
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'xgboost_vital_signs_model.json')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
LABEL_ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'label_encoder.pkl')

model = xgb.XGBClassifier()
model.load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)

def predict_my_health(request):
    if request.method == "POST":
        # Get latest patient data from database
        patient = PatientInfo.objects.latest('id')

        # Convert data to DataFrame
        patient_data = pd.DataFrame([{
            'HeartRate': patient.heart_rate,
            'BloodPressure_Systolic': patient.blood_pressure_systolic,
            'BloodPressure_Diastolic': patient.blood_pressure_diastolic,
            'OxygenSaturation': patient.oxygen_saturation,
            'Temperature': patient.temperature,
            'RespiratoryRate': patient.respiratory_rate
        }])

        # Scale the input
        patient_scaled = scaler.transform(patient_data)

        # Predict using the trained model
        prediction = model.predict(patient_scaled)

        # Decode label
        health_status = label_encoder.inverse_transform(prediction)[0]

        return render(request, "predict_health.html", {"health_status": health_status})

    return render(request, "predict_health.html")

# def patients_list(request):
#     patients = Patient.objects.all()  # Fetch all patients from the database
#     return render(request, 'patients_list.html', {'patients': patients})

@csrf_exempt  # Only for testing, use proper CSRF protection in production
def add_patient_details(request):
    if request.method == "POST":
        # Get extracted data from the request
        first_name = request.POST.get("first_name", "Unknown")
        last_name = request.POST.get("last_name", "Unknown")
        age = request.POST.get("age", "0")
        gender = request.POST.get("gender", "Unknown")
        phone_number = request.POST.get("phone_number", "")
        body_temperature = request.POST.get("body_temperature", "")
        spo2 = request.POST.get("spo2", "")
        heart_rate = request.POST.get("heart_rate", "")
        respiration_rate = request.POST.get("respiration_rate", "")
        blood_pressure_systolic = request.POST.get("blood_pressure_systolic", "")
        blood_pressure_diastolic = request.POST.get("blood_pressure_diastolic", "")

        # Save extracted data to the Patient model
        new_patient = Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=int(age),
            gender=gender,
            phone_number=phone_number,
            body_temperature=body_temperature,
            spo2=int(spo2),
            heart_rate=int(heart_rate),
            respiration_rate=int(respiration_rate),
            blood_pressure_systolic=int(blood_pressure_systolic),
            blood_pressure_diastolic=int(blood_pressure_diastolic),
        )

        # Redirect to the patient details page after saving
        return redirect("patient_details")

    return redirect("dashboard")  # Redirect if accessed via GET


def save_patient_details(request):
    if request.method == "POST":
        # Create and save a new Patient object with extracted data
        patient = Patient.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            age=request.POST.get("age"),
            gender=request.POST.get("gender"),
            phone_number=request.POST.get("phone_number"),
            body_temperature=request.POST.get("body_temperature"),
            spo2=request.POST.get("spo2"),
            heart_rate=request.POST.get("heart_rate"),
            respiration_rate=request.POST.get("respiration_rate"),
            blood_pressure_systolic=request.POST.get("blood_pressure_systolic"),
            blood_pressure_diastolic=request.POST.get("blood_pressure_diastolic")
        )

        # Redirect to Patient Details page after saving
        return redirect("patient_details")

    return redirect("dashboard")  # Redirect to dashboard if accessed via GET

from django.shortcuts import render
from .models import Patient  # Ensure you have a Patient model

def dashboard_view(request):
    total_patients = Patient.objects.count()  # Get total number of patients
    return render(request, 'dashboard.html', {'total_patients': total_patients})

from django.http import JsonResponse

def get_patient_count(request):
    total_patients = Patient.objects.count()
    return JsonResponse({'total_patients': total_patients})

