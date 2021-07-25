from django.urls import path, include
from api import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    path('frontendquestions/', views.sendfrontendquestions),
    path('backendquestions/', views.sendbackendquestions),
    path('appquestions/', views.sendappquestions),
    path('mlquestions/', views.sendmlquestions),
    path('designquestions/', views.senddesignquestions),
    path('uiuxquestions/',views.senduiuxquestions),
    path('videoquestions/',views.sendvideoquestions),

    path('send_front_responses/', views.SendFrontResponsesAPIView, name="send_front_responses"),
    path('send_back_responses/', views.SendBackResponsesAPIView, name="send_back_responses"),
    path('send_app_responses/', views.SendAppResponsesAPIView, name="send_app_responses"),
    path('send_ml_responses/', views.SendMlResponsesAPIView, name="send_ml_responses"),
    path('send_desg_responses/', views.SendDesignResponsesAPIView, name="send_desg_responses"),
    path('send_uiux_responses/',views.SendUiuxResponsesAPIView, name="send_uiux_responses"),
    path('send_video_responses/',views.SendVideoResponsesAPIView, name="send_video_responses"),

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
