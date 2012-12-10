import datetime
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail.message import EmailMessage
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

class Events(models.Model):
    
    class Meta:
        verbose_name_plural = "Events"
        
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    start_datetime = models.DateTimeField('start datetime')
    end_datetime = models.DateTimeField('end datetime')
    created_datetime = models.DateTimeField(default=datetime.now)
    
    attendees = models.ManyToManyField(User, through='Attendee')
    
    def is_over(self):
        return timezone.now() >= self.end_datetime

    def __unicode__(self):
        return self.name

class Attendee(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Events)
    is_managing = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.user.username + " => " + self.event.name

class Comment(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Events)
    comment = models.CharField(max_length=1000)
    created_datetime = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.comment
    
class Task(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    event = models.ForeignKey(Events)
    is_done = models.BooleanField(default=False)
    
    def inform_task_to_attendee(self):
    
        if self.user.email:
            assignee = self.user
            event = self.event
        
            ctx_dict = {'username': assignee.username,
                        'task_name': self.name,
                        'event_name': event.name,
                        'event_id' : event.pk,
                        'site': Site.objects.get_current()
                        }
        
            subject = event.name + " task assignment"
            message = render_to_string('eventsAtEPAM/task_message.txt',
                                       ctx_dict)
        
            try:
              mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [self.user.email])
              mail.send()
              print 'email sent for task: ' + self.name
            except: 
              print 'There was an error sending your invitation.'
    
    def save(self, *args, **kwargs):
        attendee, created = Attendee.objects.get_or_create(user=self.user, event=self.event)
        attendee.is_managing = True
        attendee.save()
        if not self.pk:
            self.inform_task_to_attendee()
        super(Task, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name

class Subscriber(models.Model):
    
    FREQUENCY_CHOICES = (
        ('d', 'Daily Digest'),
        ('w', 'Weekly Digest'),
    )
    
    FILTER_CHOICES = (
        ('m', 'Just My Events'),
        ('a', 'All Events in my Area'),
        ('c', 'All Events in EPAM'),
    )
    
    user = models.ForeignKey(User)
    frequency = models.CharField(max_length=2,
                                      choices=FREQUENCY_CHOICES,
                                      default='d')
    event_filter = models.CharField(max_length=2,
                                      choices=FILTER_CHOICES,
                                      default='c')
    
    