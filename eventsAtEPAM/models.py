import datetime
from django.db import models
from django.utils import timezone
from datetime import datetime

class Events(models.Model):
    
    class Meta:
        verbose_name_plural = "Events"
        
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    start_datetime = models.DateTimeField('start datetime')
    end_datetime = models.DateTimeField('end datetime')
    created_datetime = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.name