from rest_framework import viewsets,generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Domain,mcqQuestions,typeQuestions,Responses, User
from .serializers import (mcqSerializer, typeSerializer,
                            RegisterSerializer,LoginSerializer,
                            responseSerializer, LogoutSerializer,
                            EmailVerificationSerializer,
                            ResetPasswordEmailRequestSerializer,
                            SetNewPasswordSerializer)
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
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

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
        email_body = 'Hi '+ user.username +  ' Use the OTP below to verify your email \n' + str(user_otp)
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email for MFC recruitment portal'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    def post(self, request):
        otp = request.data['otp']
        email = request.data['email']
        try:
            user = User.objects.get(email = email)
            if otp == user.otp:
                if not user.is_verified:
                    user.is_verified = True
                    user.save()
                    email_body = '<h1> Hello ' + user.username + ', Greetings from MFCVIT, </h1>' + 'Your account has been successfully activated. \n' + 'You can now go to recruitment portal and attempt test for all domains.'
                    data = {'email_body': email_body, 'to_email': user.email,
                            'email_subject': 'Account activation successful'}
                    Util.send_email(data)
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

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email', '')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('api:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})[19:]
            redirect_url = request.data.get('redirect_url', '')
            absurl = 'https://recruitments.mfcvit.in/user/newpassword' + relativeLink
            email_body = '<h1>Greetings from MFC VIT</h1> \n Use link below to reset your password  \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)

# class PasswordTokenCheckAPI(generics.GenericAPIView):
#     serializer_class = SetNewPasswordSerializer
#     def get(self, request, uidb64, token):
#         redirect_url = request.GET.get('redirect_url')
#         try:
#             id = smart_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 if len(redirect_url) > 3:
#                     return CustomRedirect(redirect_url+'?token_valid=False')
#                 else:
#                     return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')
#             if redirect_url and len(redirect_url) > 3:
#                 return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
#             else:
#                 return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')
#         except DjangoUnicodeDecodeError as identifier:
#             try:
#                 if not PasswordResetTokenGenerator().check_token(user):
#                     return CustomRedirect(redirect_url+'?token_valid=False')
#             except UnboundLocalError as e:
#                 return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is not valid, please request a new one'}, status = status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True,'message':'Credentials Valid','uidb64': uidb64, 'token':token},status = status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error':'Token is not valid, please request a new one'}, status = status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success':'User successfully logged out'},status=status.HTTP_200_OK)
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
        user = request.user
        user.technical_test = True
        user.save()
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
        user = request.user
        user.management_test = True
        user.save()
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
                'error': 'User already attempted Editorial Test'
            }
            return Response(error)
        user = request.user
        user.editorial_test = True
        user.save()
        ed_domain = Domain.objects.get(domain_name='Editorial')
        type = typeQuestions.objects.filter(domain=ed_domain)
        shortquestions = []
        longquestions = []
        for question in type:
            if 'ed_long' in question.question_id:
                longquestions.append(question)
            else:
                shortquestions.append(question)
        random_short = random.sample(list(shortquestions), 3)
        random_long = random.sample(list(longquestions), 3)
        typeshortserializer = typeSerializer(random_short, many=True)
        typelongserializer = typeSerializer(random_long, many=True)
        finalquestions = {
            'write': {
                'long': typelongserializer.data,
                'short': typeshortserializer.data
            }
        }
        return Response(finalquestions)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def senddesignquestions(request):
    if request.method == 'GET':
        if request.user.design_test:
            error = {
                'error': 'User already attempted Design Test'
            }
            return Response(error)
        user = request.user
        user.design_test = True
        user.save()
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
        # if request.user.technical_test:
        #     error = {
        #         'error': 'User already attempted Technical Test'
        #     }
        #     return Response(error)
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
        # if request.user.management_test:
        #     error = {
        #         'error': 'User already attempted Management Test'
        #     }
        #     return Response(error)
        if serializer.is_valid():
            serializer.save(user=request.user)
            user = request.user
            user.management_test = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SendEditorialResponsesAPIView(request):
    if request.method == 'POST':
        serializer = responseSerializer(data=request.data,many=True)
        # if request.user.editorial_test:
        #     error = {
        #         'error': 'User already attempted Editorial Test'
        #     }
        #     return Response(error)
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
        # if request.user.design_test:
        #     error = {
        #         'error': 'User already attempted Design Test'
        #     }
        #     return Response(error)
        if serializer.is_valid():
            serializer.save(user=request.user)
            user = request.user
            user.design_test = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
