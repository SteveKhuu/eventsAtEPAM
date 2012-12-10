import icalendar
import random
import sys
from icalendar import Calendar, Event

from django import forms
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from eventsAtEPAM.models import Events, Attendee, Comment, Task
from eventsAtEPAM.eventForms import EventForm, CommentForm, AddTaskFormset, TaskForm

def index(request):
    events = Events.objects.all().order_by('-start_datetime')
    
    context = {
               'events' : events
               }
    
    return render(request, 'eventsAtEPAM/index.html', context)

def my_events(request):
    user = request.user
    events = Events.objects.filter(attendees=user).order_by('-start_datetime')
    
    context = {
               'events' : events
               }
    
    return render(request, 'eventsAtEPAM/index.html', context)

def attend_event(request, event_id):
    event = Events.objects.get(pk=event_id)
    attendee = Attendee(user=request.user, event=event)
    attendee.save()
    
    return redirect('detail', event_id=event_id)

def leave_event(request, event_id):
    event = Events.objects.get(pk=event_id)
    
    attendee = Attendee.objects.get(user=request.user, event=event)
    attendee.delete()
    
    return redirect('detail', event_id=event_id)

def detail(request, event_id):
    user = request.user
    event = get_object_or_404(Events, pk=event_id)
    comments = Comment.objects.filter(event=event)
    attendees = Attendee.objects.filter(event=event)
    
    is_attending = event.attendees.filter(username=request.user.username).exists()
    is_managing = False
    
    task_list_formset = []
    
    if is_attending:
        attendee = Attendee.objects.get(event=event, user=request.user)
        
        is_managing = is_managing or attendee.is_managing
        
        if is_managing:
            
            tasks = Task.objects.filter(event=event)
            task_list_formset = AddTaskFormset(prefix='task', instance=event)
            
            if request.method=='POST':
        
              task_list_formset = AddTaskFormset(request.POST, prefix='task', instance=event)
              
              if task_list_formset.is_valid():
                task_list_formset.save()
                task_list_formset = AddTaskFormset(prefix='task', instance=event)
              else:
                  print 'invalid formset'
                  print task_list_formset.errors
    
    comment_form = CommentForm(initial={'event':event.pk, 'user':request.user.id})
    
    context = {
               'event' : event,
               'attendees' : attendees,
               'comments' : comments,
               'is_attending' : is_attending,
               'is_managing' : is_managing,
               'comment_form' : comment_form,
               'task_list_formset' : task_list_formset,
               }
    
    return render(request, 'eventsAtEPAM/detail.html', context)

def create_event(request):
    
    form = EventForm()
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save()
            attendee = Attendee(user = request.user, event = new_event, is_managing=True)
            attendee.save()
            return redirect('detail', event_id=new_event.pk)
        
    context = {
               'form' : form,
               'button_label' : 'Create Event'
    }
    return render(request, 'eventsAtEPAM/create.html', context)
                
def edit_event(request, event_id):
    
    event = get_object_or_404(Events, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            new_event = form.save()
            return redirect('detail', event_id=new_event.pk)
        else:
            form = EventForm()
        
    else:
        form = EventForm(instance=event)
        
    context = {
    'form' : form,
    'button_label' : 'Save changes'
    }
    return render(request, 'eventsAtEPAM/create.html', context)

def make_calendar_object(event_id):
    event = get_object_or_404(Events, pk=event_id)

    site = Site.objects.get_current()

    site_token = site.domain.split('.')
    site_token.reverse()
    site_token = '.'.join(site_token)

    cal = Calendar()
    cal.add('prodid', '-//%s Events Calendar//%s//' % (site.name, site.domain))
    cal.add('version', '2.0')

    eventObj = Event()
    eventObj.add('summary', event.name)
    eventObj.add('location', event.location)
    eventObj.add('dtstart', event.start_datetime)
    eventObj.add('dtend', event.end_datetime)
    eventObj.add('dtstamp', event.created_datetime)
    eventObj['uid'] = '%dT%d.events.%s' % (event.id, random.randrange(111111111,999999999), site_token)
    eventObj.add('priority', 5)

    cal.add_component(eventObj)

    output = ""
    for line in cal.content_lines():
        if line:
            output += line + "\n"

    return output

def export_event(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    output = make_calendar_object(event_id)
    response = HttpResponse(output, mimetype="text/calendar")
    response['Content-Disposition'] = 'attachment; filename=%s.ics' % slugify(event.name + "-" + str(event.start_datetime.year))
    
    return response

def comment(request, event_id):

  if request.method == 'POST':
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
      comment_form.save()
     
    else:
      print 'Error in comments'
      print comment_form.errors
     
  return redirect('detail', event_id=event_id)