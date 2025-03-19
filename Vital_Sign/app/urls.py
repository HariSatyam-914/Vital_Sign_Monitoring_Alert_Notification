from . import views
from django.urls import path

urlpatterns = [
    path('', views.home,name='home'),
    #path('login/', views.login_view,name='login'),
    path('logout/', views.logout_view,name='logout'),
    
]

