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
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('api:email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+ user.username + ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

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
