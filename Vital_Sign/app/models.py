from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    body_temperature = models.CharField(max_length=10)
    spo2 = models.IntegerField()
    heart_rate = models.IntegerField()
    respiration_rate = models.IntegerField()
    blood_pressure_systolic = models.IntegerField()
    blood_pressure_diastolic = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return(f"{self.first_name} {self.last_name} {self.age} {self.gender} {self.phone_number} {self.body_temperature} {self.spo2} {self.heart_rate} {self.respiration_rate} {self.blood_pressure_systolic} {self.blood_pressure_diastolic}")

class PatientReport(models.Model):
    patient_name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    body_temperature = models.FloatField()
    spo2 = models.FloatField()
    heart_rate = models.IntegerField()
    respiration_rate = models.IntegerField()
    blood_pressure_systolic = models.IntegerField()
    blood_pressure_diastolic = models.IntegerField()
    
    # File field for PDF report
    report_pdf = models.FileField(upload_to='medical_reports/', null=True, blank=True)

    def __str__(self):
        return self.patient_name
    
class PatientInfo(models.Model):
    patient_name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    body_temperature = models.FloatField()
    spo2 = models.FloatField()
    heart_rate = models.IntegerField()
    respiration_rate = models.IntegerField()
    blood_pressure_systolic = models.IntegerField()
    blood_pressure_diastolic = models.IntegerField()

    def __str__(self):
        return self.patient_name