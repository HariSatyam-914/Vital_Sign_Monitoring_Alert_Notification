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

