from django.contrib import admin
from .models import Department,Patient,Doctor,Diagnosis,Appointment
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):list_display=('id','name');search_fields=('name',)
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):list_display=('id','name','phone','birth_date');search_fields=('name','phone')
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):list_display=('id','name','specialty','department');list_filter=('department',);search_fields=('name','specialty');list_select_related=('department',)
@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):list_display=('id','name','code');search_fields=('name','code')
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display=('id','patient','doctor','date','time','status')
    list_filter=('status','date','doctor__department')
    search_fields=('patient__name','doctor__name','notes')
    ordering=('-date','-time')
    list_select_related=('patient','doctor')
    filter_horizontal=('diagnoses',)
