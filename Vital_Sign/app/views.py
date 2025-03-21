from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import RegistrationForm
from .models import Patient

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
        Patient.objects.create(
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

        return redirect('patient_details')  # Redirect to patient details page after adding

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