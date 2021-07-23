from django.contrib import admin
from .models import (Domain,typeQuestions,Responses,User)
from django.utils.html import format_html
import csv
from django.http import HttpResponse

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

@admin.register(User)
class UserAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['username','reg_no','email','phone_number']
    actions = ["export_as_csv"]
# Register your models here.
@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain_name','id']

@admin.register(typeQuestions)
class typeQuestionsAdmin(admin.ModelAdmin):
    list_display = ['domain','question_id','get_question']

    def get_question(self, obj):
        html = "<img src='" + str(obj.question) + "' style='height:200px;width:300px' />";
        return format_html(html)
    get_question.short_description = 'question'


@admin.register(Responses)
class ResponsesAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['user','get_reg_no','domain','get_question','answer']
    list_filter = ['domain']
    search_fields = ['user__username']
    actions = ["export_as_csv"]

    def get_reg_no(self, obj):
        return obj.user.reg_no
    get_reg_no.short_description = 'reg_no'

    def get_question(self, obj):
        html = "<img src='" + str(obj.question) + "' style='height:200px;width:300px' />";
        return format_html(html)
    get_question.short_description = 'question'
