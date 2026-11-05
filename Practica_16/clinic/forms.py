from django import forms
from .models import Appointment
class AppointmentForm(forms.ModelForm):
    class Meta:
        model=Appointment
        fields=['patient','doctor','date','time','status','diagnoses','notes']
        widgets={'date':forms.DateInput(attrs={'type':'date'},format='%Y-%m-%d'),'time':forms.TimeInput(attrs={'type':'time'},format='%H:%M'),'diagnoses':forms.SelectMultiple(attrs={'size':4}),'notes':forms.Textarea(attrs={'rows':3})}
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['date'].input_formats=['%Y-%m-%d']
        self.fields['time'].input_formats=['%H:%M','%H:%M:%S']
