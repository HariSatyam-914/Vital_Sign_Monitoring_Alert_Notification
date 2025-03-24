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
    path('predict-health/<int:patient_id>/', views.predict_health, name='predict_health_with_id'),  # New route
    path('upload-medical-report/', views.upload_medical_report, name='upload_medical_report'),  # ✅ Add this line
    path('add-patient/', views.add_patient, name='add_patient'),
    path('delete-patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('edit-patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('predict-health/', views.predict_health, name='predict_health'),
    path("add-extracted-data/", views.add_extracted_data, name="add_extracted_data"),
    path('add-patient-details/', views.add_patient_details, name='add_patient_details'),
    path('save-patient-details/', views.save_patient_details, name='save_patient_details'),
    path('api/get_patient_count/', views.get_patient_count, name='get_patient_count'),
    #path('dashboard/', views.dashboard, name='dashboard'),
]

