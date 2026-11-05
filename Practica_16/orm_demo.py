import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
import django
django.setup()
from django.db.models import Count,Avg
from clinic.models import Appointment,Department,Patient
print('all:',Appointment.objects.all()[:2])
print('filter:',Appointment.objects.filter(status='scheduled').count())
print('exclude:',Appointment.objects.exclude(status='cancelled').count())
print('get:',Patient.objects.get(pk=Patient.objects.first().pk))
print('order_by:',list(Appointment.objects.order_by('date').values_list('id',flat=True)[:5]))
print('count:',Appointment.objects.count())
print('exists:',Appointment.objects.exists())
print('aggregate:',Appointment.objects.aggregate(total=Count('id')))
print('annotate:',list(Department.objects.annotate(total=Count('doctors__appointments')).values('name','total')))
print('related:',list(Appointment.objects.select_related('patient','doctor').prefetch_related('diagnoses')[:2]))
