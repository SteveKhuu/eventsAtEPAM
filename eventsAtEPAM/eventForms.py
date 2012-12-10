from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import HiddenInput, Textarea
from eventsAtEPAM.models import Events, Comment, Task
from eventsAtEPAM.widgets import SplitSelectDateTimeWidget

class EventForm(ModelForm):
    class Meta:
      model = Events
      fields = ('name', 'location', 'description', 'start_datetime', 'end_datetime')
      widgets = {
        'start_datetime' : SplitSelectDateTimeWidget(),
        'end_datetime' : SplitSelectDateTimeWidget()
      }

class CommentForm(ModelForm):

    comment = forms.CharField(widget=forms.Textarea, label='')
   
    class Meta:
      model = Comment
      fields = ('user', 'event', 'comment')
      widgets = {
        'event' : HiddenInput(),
        'user' : HiddenInput(),
      }

class TaskForm(ModelForm):
    fields = ('name', 'user', 'is_done')
    class Meta:
      model = Task
      widgets = {
        'created_datetime' : HiddenInput()
      }


AddTaskFormset = inlineformset_factory(Events, Task, form=TaskForm, extra=1, can_delete=False)
