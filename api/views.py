from rest_framework import viewsets,generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Domain,mcqQuestions,typeQuestions,Responses, User
from .serializers import (mcqSerializer, typeSerializer,
                            RegisterSerializer,LoginSerializer,
                            responseSerializer, LogoutSerializer,
                            EmailVerificationSerializer)
from rest_framework.generics import ListCreateAPIView
import random
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.shortcuts import redirect
from .renderers import UserRenderer

# Create your views here.
##########################################################


def generate_otp():
    key = random.randint(100,999)
    counter = random.randint(100,999)
    otp_str = str(key) + str(counter)
    otp = int(otp_str)
    return otp

###########################################################
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        user_otp = generate_otp()
        user.otp = user_otp
        user.save()
        token = RefreshToken.for_user(user).access_token
        email_body = 'Hi '+ user.username + ' Use the OTP below to verify your email \n' + str(user_otp)
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email for MFC recruitment portal'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    # otp_param_config = openapi.Parameter(
    #     'otp', in_=openapi.IN_QUERY, description='Enter OTP', type=openapi.TYPE_STRING)
    # @swagger_auto_schema(manual_parameters=[otp_param_config])
    def post(self, request):
        otp = request.data['otp']
        email = request.data['email']
        try:
            user = User.objects.get(email = email)
            if otp == user.otp:
                if not user.is_verified:
                    user.is_verified = True
                    user.save()
                return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Invalid OTP or Email'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


###################################

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_tests(request):
    user = request.user
    tests = {
        'technical': user.technical_test,
        'management': user.management_test,
        'editorial': user.editorial_test,
        'design': user.design_test,
    }
    return Response(tests)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sendtechnicalquestions(request):
    if request.method == 'GET':
        if request.user.technical_test:
            error = {
                'error': 'User already attempted Technical Test'
            }
            return Response(error)
        tech_domain = Domain.objects.get(domain_name='Technical')
        mcqs = mcqQuestions.objects.filter(domain=tech_domain)
        finalmcqs = random.sample(list(mcqs), 10)
        mcqserializer = mcqSerializer(finalmcqs, many=True)
        type = typeQuestions.objects.filter(domain=tech_domain)
        finaltype = random.sample(list(type), 2)
        typeserializer = typeSerializer(finaltype, many=True)
        finalquestions = {
            'mcq':mcqserializer.data,
            'write':typeserializer.data
        }
        return Response(finalquestions)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sendmanagementquestions(request):
    if request.method == 'GET':
        if request.user.management_test:
            error = {
                'error': 'User already attempted Management Test'
            }
            return Response(error)
        mang_domain = Domain.objects.get(domain_name='Management')
        type = typeQuestions.objects.filter(domain=mang_domain)
        finaltype = random.sample(list(type), 5)
        typeserializer = typeSerializer(finaltype, many=True)
        finalquestions = {
            'write':typeserializer.data
        }
        return Response(finalquestions)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sendeditorialquestions(request):
    if request.method == 'GET':
        if request.user.editorial_test:
            error = {
                'error': 'User already attempted Management Test'
            }
            return Response(error)
        ed_domain = Domain.objects.get(domain_name='Editorial')
        type = typeQuestions.objects.filter(domain=ed_domain)
        finaltype = random.sample(list(type), 2)
        typeserializer = typeSerializer(finaltype, many=True)
        finalquestions = {
            'write':typeserializer.data
        }
        return Response(finalquestions)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def senddesignquestions(request):
    if request.method == 'GET':
        if request.user.design_test:
            error = {
                'error': 'User already attempted Management Test'
            }
            return Response(error)
        design_domain = Domain.objects.get(domain_name='Design')
        finaltype = typeQuestions.objects.filter(domain=design_domain)
        typeserializer = typeSerializer(finaltype, many=True)
        finalquestions = {
            'write':typeserializer.data
        }
        return Response(finalquestions)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SendTechnicalResponsesAPIView(request):
    if request.method == 'POST':
        serializer = responseSerializer(data=request.data,many=True)
        if request.user.technical_test:
            error = {
                'error': 'User already attempted Technical Test'
            }
            return Response(error)
        if serializer.is_valid():
            serializer.save(user=request.user)
            user = request.user
            user.technical_test = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SendManagementResponsesAPIView(request):
    if request.method == 'POST':
        serializer = responseSerializer(data=request.data,many=True)
        if request.user.management_test:
            error = {
                'error': 'User already attempted Management Test'
            }
            return Response(error)
        if serializer.is_valid():
            serializer.save(user=request.user)
            user = request.user
            user.technical_test = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SendEditorialResponsesAPIView(request):
    if request.method == 'POST':
        serializer = responseSerializer(data=request.data,many=True)
        if request.user.editorial_test:
            error = {
                'error': 'User already attempted Management Test'
            }
            return Response(error)
        if serializer.is_valid():
            serializer.save(user=request.user)
            user = request.user
            user.editorial_test = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SendDesignResponsesAPIView(request):
    if request.method == 'POST':
        serializer = responseSerializer(data=request.data,many=True)
        if request.user.design_test:
            error = {
                'error': 'User already attempted Management Test'
            }
            return Response(error)
        if serializer.is_valid():
            serializer.save(user=request.user)
            user = request.user
            user.design_test = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
