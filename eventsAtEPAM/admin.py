from django.contrib import admin
from eventsAtEPAM.models import Events, Comment, Attendee, Task, Subscriber

class EventsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information',               {'fields': ['name', 'location', 'description']}),
        ('Date information', {'fields': ['start_datetime', 'end_datetime']}),
    ]
    list_display = ('name', 'is_over', 'location', 'start_datetime')
    list_filter = ['start_datetime']
    date_hierarchy = 'start_datetime'
    
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'event', 'is_done')
    
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'is_managing')

class SubscriberAdmin(admin.ModelAdmin):
    
    actions = ['test_action']
    
    def test_action(self, request, queryset):
        self.message_user(request, "This is a test.")

    

admin.site.register(Events, EventsAdmin)
admin.site.register(Comment)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
