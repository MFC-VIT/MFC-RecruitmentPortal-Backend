from rest_framework import serializers
from .models import Domain,mcqQuestions,typeQuestions,Responses
from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token


class mcqSerializer(serializers.ModelSerializer):
    class Meta:
        model = mcqQuestions
        fields = ('question_id','question','option_1','option_2','option_3','option_4')


class typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = typeQuestions
        fields = ('question_id', 'question')
