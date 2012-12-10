from django.contrib import admin
from eventsAtEPAM.models import Events, Comment, Attendee

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'is_managing')

admin.site.register(Events)
admin.site.register(Comment)
admin.site.register(Attendee, AttendeeAdmin)