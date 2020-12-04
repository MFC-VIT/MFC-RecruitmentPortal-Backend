from django.contrib import admin
from .models import (Domain,mcqQuestions,typeQuestions,Responses,User)
from django.utils.html import format_html

admin.site.register(User)

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
    list_display = ['user','domain','get_question','answer']
    list_filter = ['domain']
    search_fields = ['user__username']

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
