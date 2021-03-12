from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Room)
admin.site.register(Department)
admin.site.register(User)
admin.site.register(Event)
admin.site.register(EventParticipant)
admin.site.register(EventRating)