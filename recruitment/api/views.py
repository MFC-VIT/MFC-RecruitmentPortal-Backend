from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Domain,mcqQuestions,typeQuestions,Responses
from .serializers import mcqSerializer, typeSerializer
import random

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
