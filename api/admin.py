from django.contrib import admin
from .models import (Domain,mcqQuestions,typeQuestions,Responses,User)
from django.utils.html import format_html

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','reg_no','email','phone_number']
# Register your models here.
@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain_name','id']

@admin.register(mcqQuestions)
class mcqQuestionsAdmin(admin.ModelAdmin):
    list_display = ['domain','question_id','get_question']

    def get_question(self, obj):
        html = "<img src='" + str(obj.question) + "' style='height:200px;width:300px' />";
        return format_html(html)
    get_question.short_description = 'question'

@admin.register(typeQuestions)
class typeQuestionsAdmin(admin.ModelAdmin):
    list_display = ['domain','question_id','get_question']

    def get_question(self, obj):
        html = "<img src='" + str(obj.question) + "' style='height:200px;width:300px' />";
        return format_html(html)
    get_question.short_description = 'question'


@admin.register(Responses)
class ResponsesAdmin(admin.ModelAdmin):
    list_display = ['user','get_reg_no','domain','get_question','answer']
    list_filter = ['domain']
    search_fields = ['user__username']

    def get_reg_no(self, obj):
        return obj.user.reg_no
    get_reg_no.short_description = 'reg_no'

    def get_question(self, obj):
        html = "<img src='" + str(obj.question) + "' style='height:200px;width:300px' />";
        return format_html(html)
    get_question.short_description = 'question'


# class MyModelAdmin(admin.ModelAdmin):
#     ...
#
#     list_display = ['get_description', ]
#
#     def get_description(self, obj):
#        return format_html(obj)
#     get_description.short_description = 'description'
