from datetime import date,time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Department,Doctor,Patient,Appointment,Diagnosis
class ClinicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dep=Department.objects.create(name='Терапия')
        cls.doc=Doctor.objects.create(name='Иванов',department=cls.dep,specialty='Терапевт')
        cls.patient=Patient.objects.create(name='Петров',phone='123')
        cls.diag=Diagnosis.objects.create(name='ОРВИ')
        cls.a=Appointment.objects.create(patient=cls.patient,doctor=cls.doc,date=date(2026,12,1),time=time(10),status='scheduled')
        cls.a.diagnoses.add(cls.diag)
        User=get_user_model()
        cls.viewer=User.objects.create_user('viewer',password='test12345')
        cls.admin=User.objects.create_user('admin',password='test12345',is_staff=True,is_superuser=True)
    def test_home(self):self.assertEqual(self.client.get('/').status_code,200)
    def test_list(self):self.assertContains(self.client.get('/appointments/'),'Петров')
    def test_detail(self):self.assertContains(self.client.get(f'/appointments/{self.a.pk}/'),'Иванов')
    def test_search(self):self.assertContains(self.client.get('/appointments/?q=Петров'),'Петров')
    def test_search_no_match(self):self.assertNotContains(self.client.get('/appointments/?q=Несуществующий'),'Петров')
    def test_filter_status(self):self.assertContains(self.client.get('/appointments/?status=scheduled'),'Петров')
    def test_filter_department(self):self.assertContains(self.client.get(f'/appointments/?department={self.dep.pk}'),'Петров')
    def test_sort(self):self.assertEqual(self.client.get('/appointments/?sort=date').status_code,200)
    def test_pagination(self):self.assertContains(self.client.get('/appointments/'),'Страница 1')
    def test_statistics(self):self.assertContains(self.client.get('/statistics/'),'Запланировано')
    def test_history(self):self.assertContains(self.client.get(f'/patients/{self.patient.pk}/history/'),'Иванов')
    def test_anonymous_cannot_create(self):self.assertEqual(self.client.get('/appointments/create/').status_code,302)
    def test_viewer_cannot_create(self):self.client.force_login(self.viewer);self.assertEqual(self.client.get('/appointments/create/').status_code,403)
    def test_admin_can_create(self):self.client.force_login(self.admin);self.assertEqual(self.client.get('/appointments/create/').status_code,200)
    def test_create_post(self):
        self.client.force_login(self.admin)
        response=self.client.post('/appointments/create/',{'patient':self.patient.pk,'doctor':self.doc.pk,'date':'2026-12-02','time':'11:00','status':'scheduled','notes':''})
        self.assertEqual(response.status_code,302);self.assertEqual(Appointment.objects.count(),2)
    def test_validation(self):
        self.client.force_login(self.admin)
        response=self.client.post('/appointments/create/',{'patient':self.patient.pk,'doctor':self.doc.pk,'date':'bad','time':'11:00','status':'scheduled'})
        self.assertEqual(response.status_code,200);self.assertEqual(Appointment.objects.count(),1)
    def test_update(self):
        self.client.force_login(self.admin)
        response=self.client.post(f'/appointments/{self.a.pk}/edit/',{'patient':self.patient.pk,'doctor':self.doc.pk,'date':'2026-12-01','time':'10:00','status':'completed','notes':''})
        self.assertEqual(response.status_code,302);self.a.refresh_from_db();self.assertEqual(self.a.status,'completed')
    def test_delete(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.post(f'/appointments/{self.a.pk}/delete/').status_code,302)
        self.assertFalse(Appointment.objects.exists())
    def test_relationship(self):self.assertEqual(self.a.diagnoses.count(),1)
    def test_admin_login(self):self.assertEqual(self.client.get('/admin/login/').status_code,200)
