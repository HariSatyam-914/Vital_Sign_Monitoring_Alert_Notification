import pdfplumber
import re
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import RegistrationForm
from .models import Patient
from .forms import PatientReportForm
from .utils import extract_patient_data  # Import the extraction function
from .models import PatientReport
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from .models import PatientInfo
import csv
from django.http import HttpResponse
import logging
import numpy as np
import joblib
import tensorflow as tf


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


def predict_health(request):
    return render(request, 'predict_health.html')

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
    extracted_data = None  # Initialize extracted data

    if request.method == "POST" and request.FILES.get("medical_report"):
        uploaded_file = request.FILES["medical_report"]
        fs = FileSystemStorage()
        file_path = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(file_path)

        extracted_data = extract_patient_data(file_path)  # Extract info from PDF

        # Save data to database (Optional)
        patient = PatientInfo.objects.create(
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
        patient.save()

    return render(request, "upload_medical_report.html", {"extracted_data": extracted_data})


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


# Load trained LSTM model & scaler
model = tf.keras.models.load_model("/mnt/data/lstm_health_model.h5")
scaler = joblib.load("/mnt/data/scaler.pkl")

def predict_health(request):
    patients = Patient.objects.all()  # Fetch patient records from DB
    
    predictions = []

    for patient in patients:
        # Prepare data for LSTM (same feature order as training)
        input_data = np.array([[patient.body_temperature, patient.spo2, patient.heart_rate,
                                 patient.respiration_rate, patient.blood_pressure_systolic, 
                                 patient.blood_pressure_diastolic]])
        
        # Normalize data
        input_data = scaler.transform(input_data)
        input_data = input_data.reshape((1, 1, input_data.shape[1]))  # Reshape for LSTM

        # Predict
        prediction = model.predict(input_data)
        predicted_class = np.argmax(prediction)  # Get class with highest probability

        # Convert class to label
        status = {0: "Healthy", 1: "At Risk", 2: "Diseased"}
        predictions.append({"patient": patient, "health_status": status[predicted_class]})

    return render(request, "predict_health.html", {"predictions": predictions})