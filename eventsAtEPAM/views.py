from django.shortcuts import render, get_object_or_404
from eventsAtEPAM.models import Events

def index(request):
    events = Events.objects.all()
    
    context = {
               'events' : events
               }
    
    return render(request, 'eventsAtEPAM/index.html', context)