from django.contrib import admin
from .models import Team, JoinRequest, Invite

# Register your models here.
admin.site.register(Team)
admin.site.register(JoinRequest)
admin.site.register(Invite)