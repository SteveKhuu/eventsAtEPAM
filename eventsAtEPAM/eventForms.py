from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from eventsAtEPAM.models import Events
from eventsAtEPAM.widgets import SplitSelectDateTimeWidget

class EventForm(ModelForm):
    class Meta:
      model = Events
      fields = ('name', 'location', 'description', 'start_datetime', 'end_datetime')
      widgets = {
        'start_datetime' : SplitSelectDateTimeWidget(),
        'end_datetime' : SplitSelectDateTimeWidget()
      }