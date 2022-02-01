from django.urls import path
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
    path('mediaquestions/', views.sendmediaquestions),
    path('send_tech_responses/', views.SendTechnicalResponsesAPIView, name="send_tech_responses"),
    path('send_mang_responses/', views.SendManagementResponsesAPIView, name="send_mang_responses"),
    path('send_edit_responses/', views.SendEditorialResponsesAPIView, name="send_edit_responses"),
    path('send_desg_responses/', views.SendDesignResponsesAPIView, name="send_desg_responses"),
    path('send_media_responses/', views.SendMediaResponsesAPIView, name="send_media_responses"),
    path('register/',views.RegisterView.as_view(),name="register"),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user_test/',views.user_tests, name="user_tests"),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(),name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', views.SetNewPasswordAPIView.as_view(),name='password-reset-complete')
]
