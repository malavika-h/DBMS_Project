from django.contrib import admin
from .models import Session, Class, Notice, Event

admin.site.register(Session)
admin.site.register(Class)
admin.site.register(Notice)
admin.site.register(Event)