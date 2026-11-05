from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q,Count,Avg
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Appointment,Patient,Doctor,Department,Diagnosis
from .forms import AppointmentForm

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):return self.request.user.is_authenticated and self.request.user.is_staff

def home(request):
    return render(request,'clinic/home.html',{'patients':Patient.objects.count(),'doctors':Doctor.objects.count(),'appointments':Appointment.objects.count(),'departments':Department.objects.count()})

class AppointmentList(ListView):
    model=Appointment
    template_name='clinic/list.html'
    context_object_name='items'
    paginate_by=10
    def get_queryset(self):
        qs=Appointment.objects.select_related('patient','doctor','doctor__department').prefetch_related('diagnoses').all()
        q=self.request.GET.get('q','').strip()
        if q:qs=qs.filter(Q(patient__name__icontains=q)|Q(doctor__name__icontains=q))
        status=self.request.GET.get('status','')
        if status in dict(Appointment.STATUS):qs=qs.filter(status=status)
        department=self.request.GET.get('department','')
        if department.isdigit():qs=qs.filter(doctor__department_id=int(department))
        sort=self.request.GET.get('sort','')
        if sort in ['date','-date','patient__name','-patient__name']:qs=qs.order_by(sort,'id')
        return qs
    def get_context_data(self,**kwargs):
        ctx=super().get_context_data(**kwargs)
        ctx['departments']=Department.objects.all()
        ctx['statuses']=Appointment.STATUS
        ctx['params']=self.request.GET.copy()
        ctx['params'].pop('page',None)
        ctx['querystring']=ctx['params'].urlencode()
        return ctx

class AppointmentDetail(DetailView):
    model=Appointment
    template_name='clinic/detail.html'
    context_object_name='item'
    def get_queryset(self):return super().get_queryset().select_related('patient','doctor','doctor__department').prefetch_related('diagnoses')

class AppointmentCreate(StaffRequiredMixin,CreateView):
    model=Appointment;form_class=AppointmentForm;template_name='clinic/form.html';success_url=reverse_lazy('appointment-list')
class AppointmentUpdate(StaffRequiredMixin,UpdateView):
    model=Appointment;form_class=AppointmentForm;template_name='clinic/form.html';success_url=reverse_lazy('appointment-list')
class AppointmentDelete(StaffRequiredMixin,DeleteView):
    model=Appointment;template_name='clinic/delete.html';success_url=reverse_lazy('appointment-list')

def statistics(request):
    return render(request,'clinic/statistics.html',{'total':Appointment.objects.count(),'scheduled':Appointment.objects.filter(status='scheduled').count(),'completed':Appointment.objects.filter(status='completed').count(),'cancelled':Appointment.objects.filter(status='cancelled').count(),'by_department':Department.objects.annotate(total=Count('doctors__appointments',distinct=True)).order_by('-total'),'doctors':Doctor.objects.count()})

def history(request,pk):
    patient=Patient.objects.get(pk=pk)
    return render(request,'clinic/history.html',{'patient':patient,'items':Appointment.objects.filter(patient=patient).select_related('doctor').prefetch_related('diagnoses')})
