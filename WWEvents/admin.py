from django.contrib import admin
from django.forms import ModelForm

# Register your models here.
from .models import *

admin.site.register(Room)
admin.site.register(Department)

# User
class UserAdminForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['dep'].queryset = Department.objects.filter(active=True)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	form = UserAdminForm

# Event
class EventAdminForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['host'].queryset = User.objects.filter(active=True)
		self.fields['room'].queryset = Room.objects.filter(active=True)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	form = EventAdminForm

# EventParticipant
class EventParticipantAdminForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['user'].queryset = User.objects.filter(active=True)

@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
	form = EventParticipantAdminForm


admin.site.register(EventRating)