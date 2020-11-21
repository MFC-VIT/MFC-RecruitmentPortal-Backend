from django.contrib import admin
from .models import (Domain,mcqQuestions,typeQuestions,Responses)


# Register your models here.
@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain_name']

@admin.register(mcqQuestions)
class mcqQuestionsAdmin(admin.ModelAdmin):
    list_display = ['domain','question_id','question']

@admin.register(typeQuestions)
class typeQuestionsAdmin(admin.ModelAdmin):
    list_display = ['domain','question_id','question']

@admin.register(Responses)
class ResponsesAdmin(admin.ModelAdmin):
    list_display = ['user','domain','question','answer']
    list_filter = ['domain']
    search_fields = ['user__username']
