from rest_framework import viewsets,generics,status,views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Domain,mcqQuestions,typeQuestions,Responses, User
from .serializers import mcqSerializer, typeSerializer,RegisterSerializer,LoginSerializer
import random
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
# from .utils import Util
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        # user = User.objects.get(email=user_data['email'])
        # token=RefreshToken.for_user(user).access_token
        #
        # current_site = get_current_site(request).domain
        # relativeLink = reverse('email-verify')
        #
        # absurl = 'http://' + current_site + relativeLink + '?token=' + str(token)
        # email_body = 'Hi' + user.username + 'Use link below to verify your email \n' + absurl
        #
        # data={'email_body':email_body, 'to_email': user.email,
        #         'email_subject': 'verify your email'}
        #
        #
        # Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

# class VerifyEmail(views.APIView):
#     serializer_class = EmailVerificationSerializer
#     token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
#
#     @swagger_auto_schema(manual_parameters=[token_param_config])
#     def get(self, request):
#         token = request.GET.get('token')
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY)
#             user = User.objects.get(id=payload['user_id'])
#             if not user.is_verified:
#                 user.is_verified = True
#                 user.save()
#             return Response({'email':'successfully activated'}, status=status.HTTP_200_OK)
#
#         except jwt.ExpiredSignatureError as identifier:
#             return Response({'error':'Activation Error'},status = status.HTTP_400_BAD_REQUEST)
#
#         except jwt.exceptions.DecodeError as identifier:
#             return Response({'error':'Invalid token'},status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


###################################

@api_view(['GET'])
def sendtechnicalquestions(request):
    if request.method == 'GET':
        tech_domain = Domain.objects.get(domain_name='Technical')
        mcqs = mcqQuestions.objects.filter(domain=tech_domain)
        finalmcqs = random.sample(list(mcqs), 2)
        mcqserializer = mcqSerializer(finalmcqs, many=True)
        type = typeQuestions.objects.filter(domain=tech_domain)
        finaltype = random.sample(list(type), 2)
        typeserializer = typeSerializer(finaltype, many=True)
        finalquestions = {
            'mcq':mcqserializer.data,
            'type':typeserializer.data
        }
        return Response(finalquestions)

@api_view(['GET'])
def sendmanagementquestions(request):
    if request.method == 'GET':
        mang_domain = Domain.objects.get(domain_name='Management')
        mcqs = mcqQuestions.objects.filter(domain=mang_domain)
        finalmcqs = random.sample(list(mcqs), 2)
        mcqserializer = mcqSerializer(finalmcqs, many=True)
        type = typeQuestions.objects.filter(domain=mang_domain)
        finaltype = random.sample(list(type), 2)
        typeserializer = typeSerializer(finaltype, many=True)
        finalquestions = {
            'mcq':mcqserializer.data,
            'type':typeserializer.data
        }
        return Response(finalquestions)
