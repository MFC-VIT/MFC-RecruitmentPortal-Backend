from django.urls import path, include
from api import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    path('technicalquestions/', views.sendtechnicalquestions),
    path('managementquestions/', views.sendmanagementquestions),
    path('editorialquestions/', views.sendeditorialquestions),
    path('designquestions/', views.senddesignquestions),
    path('send_tech_responses/', views.SendTechnicalResponsesAPIView, name="send_tech_responses"),
    path('send_mang_responses/', views.SendManagementResponsesAPIView, name="send_mang_responses"),
    path('send_edit_responses/', views.SendEditorialResponsesAPIView, name="send_edit_responses"),
    path('send_desg_responses/', views.SendDesignResponsesAPIView, name="send_desg_responses"),
    path('register/',views.RegisterView.as_view(),name="register"),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user_test/',views.user_tests, name="user_tests"),
]
