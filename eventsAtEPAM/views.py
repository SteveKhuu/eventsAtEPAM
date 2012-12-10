from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from eventsAtEPAM.models import Events, Attendee, Comment
from eventsAtEPAM.eventForms import EventForm

def index(request):
    events = Events.objects.all()
    
    context = {
               'events' : events
               }
    
    return render(request, 'eventsAtEPAM/index.html', context)

def detail(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    comments = Comment.objects.filter(event=event)
    attendees = Attendee.objects.filter(event=event)
    
    context = {
               'event' : event,
               'attendees' : attendees,
               'comments' : comments,
               }
    
    return render(request, 'eventsAtEPAM/detail.html', context)

def create_event(request):
  if request.method == 'POST':
    form = EventForm(request.POST)
    if form.is_valid():
      new_event = form.save()
      attendee = Attendee(user = request.user, event = new_event, is_managing=True)
      attendee.save()
      return redirect('detail', event_id=new_event.pk)
  else:
    form = EventForm()
    
  context = {
             'form' : form,
             'button_label' : 'Create Event'
             }
  return render(request, 'eventsAtEPAM/create.html', context) 
