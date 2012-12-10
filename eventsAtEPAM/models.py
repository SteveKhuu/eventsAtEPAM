import datetime
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

class Events(models.Model):
    
    class Meta:
        verbose_name_plural = "Events"
        
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    start_datetime = models.DateTimeField('start datetime')
    end_datetime = models.DateTimeField('end datetime')
    created_datetime = models.DateTimeField(default=datetime.now)
    
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
    created_datetime = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.name
    