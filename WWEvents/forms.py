from django.forms import ModelForm, DateTimeInput, Select, NumberInput, HiddenInput
from .models import *

class EventForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['host'].queryset = User.objects.filter(active=True)
		self.fields['room'].queryset = Room.objects.filter(active=True)

	class Meta:
		model = Event
		fields = ['date', 'host', 'room']
		widgets = {
			'date': DateTimeInput(),
			'host': Select(attrs={"class": "ui fluid dropdown"}),
			'room': Select(attrs={"class": "ui fluid dropdown"}),
		}

class ParticipantForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['user'].queryset = User.objects.filter(active=True)

	class Meta:
		model = EventParticipant
		fields = ['user', 'sausages', 'bretzels']
		widgets = {
			'user': Select(attrs={"class": "ui fluid dropdown"}),
			'sausages': NumberInput(attrs={"step": "0.5"}),
			'bretzels': NumberInput(attrs={"step": "0.5"}),
		}

class RatingForm(ModelForm):
	class Meta:
		model = EventRating
		fields = ['name', 'sausage_rating', 'bretzel_rating', 'mustard_rating', 'orga_rating']
		widgets = {
			'sausage_rating': HiddenInput(),
			'bretzel_rating': HiddenInput(),
			'mustard_rating': HiddenInput(),
			'orga_rating': HiddenInput(),
		}