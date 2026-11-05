from datetime import date,timedelta,time
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from clinic.models import Department,Patient,Doctor,Diagnosis,Appointment
class Command(BaseCommand):
    help='Создать тестовые данные и учебных пользователей'
    def handle(self,*args,**kwargs):
        deps=[Department.objects.get_or_create(name=n)[0] for n in ['Терапия','Кардиология','Неврология','Хирургия']]
        diagnoses=[Diagnosis.objects.get_or_create(name=n,defaults={'code':c})[0] for n,c in [('ОРВИ','J06.9'),('Гипертония','I10'),('Мигрень','G43'),('Профилактический осмотр','Z00')]]
        doctors=[Doctor.objects.get_or_create(name=n,defaults={'department':deps[i%4],'specialty':s})[0] for i,(n,s) in enumerate([('Иванов Пётр','Терапевт'),('Смирнова Анна','Кардиолог'),('Кузнецов Алексей','Невролог'),('Орлова Мария','Хирург')])]
        patients=[Patient.objects.get_or_create(name=f'Пациент {i:02d}',defaults={'phone':f'+7999000{i:04d}'})[0] for i in range(1,25)]
        for i in range(24):
            a,_=Appointment.objects.get_or_create(patient=patients[i],doctor=doctors[i%4],date=date(2026,12,1)+timedelta(days=i//4),time=time(9+i%4,0),defaults={'status':['scheduled','completed','cancelled'][i%3]})
            a.diagnoses.add(diagnoses[i%4])
        User=get_user_model()
        for name,staff in [('admin',True),('viewer',False)]:
            u,created=User.objects.get_or_create(username=name,defaults={'is_staff':staff,'is_superuser':staff})
            if created:u.set_password('Lab16Demo!2026');u.save()
        self.stdout.write(self.style.SUCCESS('Готово: 4 отделения, 4 врача, 24 пациента, 24 приёма. Пользователи admin/viewer.'))
