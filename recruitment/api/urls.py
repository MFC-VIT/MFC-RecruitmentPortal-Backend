from django.urls import path, include
from api import views

app_name = 'api'

urlpatterns = [
    path('technicalquestions/', views.sendtechnicalquestions),
    path('managementquestions/', views.sendmanagementquestions),
]
