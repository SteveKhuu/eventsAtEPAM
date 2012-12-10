from django.shortcuts import render, get_object_or_404
from eventsAtEPAM.models import Events, Attendee, Comment

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
