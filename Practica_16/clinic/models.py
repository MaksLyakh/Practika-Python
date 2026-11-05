from django.db import models
from django.core.validators import MinValueValidator

class Department(models.Model):
    name=models.CharField('Отделение',max_length=120,unique=True)
    def __str__(self):return self.name
    class Meta:verbose_name='Отделение';verbose_name_plural='Отделения';ordering=['name']

class Patient(models.Model):
    name=models.CharField('ФИО',max_length=160)
    phone=models.CharField('Телефон',max_length=30)
    birth_date=models.DateField('Дата рождения',null=True,blank=True)
    def __str__(self):return self.name
    class Meta:verbose_name='Пациент';verbose_name_plural='Пациенты';ordering=['name']

class Doctor(models.Model):
    name=models.CharField('ФИО',max_length=160)
    department=models.ForeignKey(Department,on_delete=models.PROTECT,related_name='doctors',verbose_name='Отделение')
    specialty=models.CharField('Специальность',max_length=100)
    def __str__(self):return self.name
    class Meta:verbose_name='Врач';verbose_name_plural='Врачи';ordering=['name']

class Diagnosis(models.Model):
    name=models.CharField('Диагноз',max_length=150,unique=True)
    code=models.CharField('Код',max_length=20,blank=True)
    def __str__(self):return self.name
    class Meta:verbose_name='Диагноз';verbose_name_plural='Диагнозы';ordering=['name']

class Appointment(models.Model):
    STATUS=[('scheduled','Запланирован'),('completed','Завершён'),('cancelled','Отменён')]
    patient=models.ForeignKey(Patient,on_delete=models.PROTECT,related_name='appointments',verbose_name='Пациент')
    doctor=models.ForeignKey(Doctor,on_delete=models.PROTECT,related_name='appointments',verbose_name='Врач')
    date=models.DateField('Дата приёма')
    time=models.TimeField('Время приёма')
    status=models.CharField('Статус',max_length=12,choices=STATUS,default='scheduled')
    diagnoses=models.ManyToManyField(Diagnosis,blank=True,related_name='appointments',verbose_name='Диагнозы')
    notes=models.TextField('Примечание',blank=True)
    def __str__(self):return f'{self.patient} - {self.doctor} ({self.date})'
    class Meta:verbose_name='Приём';verbose_name_plural='Приёмы';ordering=['-date','-time']
