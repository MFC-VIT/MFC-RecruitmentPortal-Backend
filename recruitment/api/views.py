from rest_framework import viewsets,generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Domain,mcqQuestions,typeQuestions,Responses, User
from .serializers import mcqSerializer, typeSerializer,RegisterSerializer,LoginSerializer,responseSerializer, LogoutSerializer
from rest_framework.generics import ListCreateAPIView
import random
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
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
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


###################################

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
@permission_classes([IsAuthenticated])
def sendmanagementquestions(request):
    if request.method == 'GET':
        if request.user.management_test:
            error = {
                'error': 'User already attempted Management Test'
            }
            return Response(error)
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

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
