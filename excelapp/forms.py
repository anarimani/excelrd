from django import forms
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from .models import Event

class EventForm(forms.ModelForm):
    start_date = JalaliDateField(widget=AdminJalaliDateWidget)
    end_date = JalaliDateField(widget=AdminJalaliDateWidget)

    class Meta:
        model = Event
        fields = ['start_date', 'end_date']


    