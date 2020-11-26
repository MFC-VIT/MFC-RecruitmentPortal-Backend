from django.urls import path, include
from api import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


app_name = 'api'

urlpatterns = [
    path('technicalquestions/', views.sendtechnicalquestions),
    path('managementquestions/', views.sendmanagementquestions),
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    # path('email-verify/',views.VerifyEmail.as_view(),name="email-verify"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
