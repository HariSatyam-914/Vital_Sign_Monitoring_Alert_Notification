from . import views
from django.urls import path

urlpatterns = [
    path('', views.home,name='home'),
    #path('login/', views.login_view,name='login'),
    path('logout/', views.logout_view,name='logout'),
    path('register/', views.register_view,name='register'),
    path('dashboard/', views.dashboard_view,name='dashboard'),
    path('patient-info/', views.patient_info, name='patient_info'),  
    path('patient-details/', views.patient_details, name='patient_details'),
    path('predict-health/', views.predict_health, name='predict_health'),
    path('upload-medical-report/', views.upload_medical_report, name='upload_medical_report'),  # ✅ Add this line
    path('add-patient/', views.add_patient, name='add_patient'),
    path('delete-patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('edit-patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('predict-health/', views.predict_health, name='predict_health'),
]

