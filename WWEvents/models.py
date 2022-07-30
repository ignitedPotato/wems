from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta

class Room(models.Model):
	name = models.CharField(max_length=50)
	active = models.BooleanField(default=True)

	def __str__(self):
		if self.active:
			return self.name
		else:
			return self.name + " (deactivated)"

class Department(models.Model):
	name = models.CharField(max_length=50)
	active = models.BooleanField(default=True)

	def __str__(self):
		if self.active:
			return self.name
		else:
			return self.name + " (deactivated)"

class User(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField()
	dep = models.ForeignKey(Department, verbose_name="Department", on_delete=models.PROTECT)
	active = models.BooleanField(default=True)

	def __str__(self):
		if self.active:
			return "[" + self.dep.name + "] " + self.name
		else:
			return "[" + self.dep.name + "] " + self.name + " (deactivated)"

	@property
	def get_user_standing(self):
		events = Event.objects.filter(host=self)
		plus = 0
		for event in events:
			plus += event.get_plus_for_host
		minus = EventParticipant.objects.filter(user=self).aggregate(models.Sum('sausages'))['sausages__sum']
		minus = minus if minus != None else 0
		return plus-minus

	@property
	def get_last_host_date(self):
		events = Event.objects.filter(host=self).order_by('-date')
		if len(events) > 0:
			return events[0].date.astimezone(timezone.get_default_timezone()).strftime("%d.%m.%Y %H:%M")
		else:
			return "Nie"

	@property
	def get_mood(self):
		standing = self.get_user_standing
		events = Event.objects.filter(host=self).order_by('-date')
		if len(events) > 0:
			last_hosted_delta = timezone.now() - events[0].date
			if last_hosted_delta.days < 180 and standing >= 0:
				return "green smile"
			elif last_hosted_delta.days >= 180 and standing < 0:
				return "red frown"
			else:
				return "grey meh"
		else:
			if standing < 0:
				return "red frown"
			else:
				return "grey meh"

	@property
	def get_host_count(sound):
		return Event.objects.filter(host=self).count()

	@property
	def get_avg_rating(self):
		events = Event.objects.filter(host=self)
		if len(events) == 0:
			return 0
		else:
			ratings_sum = 0
			ratings_cnt = 0
			for event in events:
				tmp_rating = event.get_avg_rating
				if tmp_rating > 0:
					ratings_sum += tmp_rating
					ratings_cnt += 1
			if ratings_cnt > 0:
				return round(ratings_sum/ratings_cnt)
			else:
				return 0

class Event(models.Model):
	date = models.DateTimeField("Zeit & Datum", unique=True)
	host = models.ForeignKey(User, on_delete=models.PROTECT)
	room = models.ForeignKey(Room, on_delete=models.PROTECT)
	reminded_next = models.BooleanField(default=False)
	reminded_rate = models.BooleanField(default=False)

	def __str__(self):
		return self.date.astimezone(timezone.get_default_timezone()).strftime("%d.%m.%Y %H:%M") + ", " + self.host.name

	@property
	def is_past(self):
		if timezone.now() > self.date:
			return True
		else:
			return False

	@property
	def get_participants(self):
		return EventParticipant.objects.filter(event=self)

	@property
	def get_people_count(self):
		count = EventParticipant.objects.filter(event=self).count()
		return count+1 if settings.COUNT_HOST_IMPLICIT else count

	@property
	def get_plus_for_host(self):
		result = EventParticipant.objects.filter(event=self).aggregate(models.Sum('sausages'))['sausages__sum']
		return result if result != None else 0

	@property
	def get_bretzels_for_host(self):
		result = EventParticipant.objects.filter(event=self).aggregate(models.Sum('bretzels'))['bretzels__sum']
		return result if result != None else 0

	@property
	def get_ratings(self):
		return EventRating.objects.filter(event=self)

	@property
	def get_avg_rating(self):
		ratings = self.get_ratings
		if len(ratings) > 0:
			ratings_sum = 0
			for rating in ratings:
				ratings_sum += rating.get_avg
			return round(ratings_sum/len(ratings))
		else:
			return 0

	def get_ics(self):
		ics = settings.ICS_TEMPLATE
		ics = ics.replace("<WW Link>", settings.WWEMS_URL)
		ics = ics.replace("<Host Name>", self.host.name)
		ics = ics.replace("<Host Mail>", self.host.email)
		ics = ics.replace("<Event Room>", self.room.name)
		ics = ics.replace("<Start Date>", self.date.astimezone(timezone.get_default_timezone()).strftime("%Y%m%dT%H%M%S"))
		ics = ics.replace("<End Date>", (self.date + timedelta(hours=1)).astimezone(timezone.get_default_timezone()).strftime("%Y%m%dT%H%M%S"))
		ics = ics.replace("<Now Date>", timezone.now().astimezone(timezone.get_default_timezone()).strftime("%Y%m%dT%H%M%S"))
		ics = ics.replace("<Time Zone>", settings.TIME_ZONE)
		ics = ics.replace("<Event Link>", settings.WWEMS_URL+"/event/"+str(self.id)+"/")
		return ics

class EventParticipant(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)

	sausages = models.FloatField("Anz. Würste", default=2)
	bretzels = models.FloatField("Anz. Brezen", default=2)

	def __str__(self):
		return self.event.date.strftime("%d.%m.%Y %H:%M") + ", " + self.user.name + ", (" + str(self.sausages) + "/" + str(self.bretzels) + ")"

class EventRating(models.Model):
	event = models.ForeignKey(Event, on_delete = models.CASCADE)
	name = models.CharField(max_length=50, default="Anonymous")

	sausage_rating = models.PositiveSmallIntegerField("Bewertung Würste", default=4, validators=[MaxValueValidator(5)])
	bretzel_rating = models.PositiveSmallIntegerField("Bewertung Bretzen", default=4, validators=[MaxValueValidator(5)])
	mustard_rating = models.PositiveSmallIntegerField("Bewertung Senf", default=4, validators=[MaxValueValidator(5)])
	orga_rating = models.PositiveSmallIntegerField("Bewertung Organisation", default=4, validators=[MaxValueValidator(5)])

	def __str__(self):
		return "[" + str((self.sausage_rating+self.bretzel_rating+self.mustard_rating+self.orga_rating)/4.0) + "] " + self.event.date.strftime("%d.%m.%Y %H:%m") + ", " + self.event.host.name

	@property
	def get_avg(self):
		return (self.sausage_rating + self.bretzel_rating + self.mustard_rating + self.orga_rating) / 4.0
