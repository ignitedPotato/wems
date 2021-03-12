from django.core.management.base import BaseCommand, CommandError
from WWEvents.models import *
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta

class Command(BaseCommand):
	help = 'Executes regular jobs. Hopefully called by cron every hour.'

	def handle(self, *args, **options):
		latest_past_event = Event.objects.order_by('-date')[:1]

		if latest_past_event:
			if latest_past_event[0].date <= (timezone.now() - timedelta(days=5, hours=23)) and latest_past_event[0].reminded_next == False:

				users = sorted(User.objects.all(),  key=lambda m: m.get_user_standing)[:1]
				self.stdout.write("Last event was " + latest_past_event[0].date.astimezone(timezone.get_default_timezone()).strftime("%d.%m.%Y %H:%M") + ". Next event not reminded! Reminding now. Next user is: " + users[0].name)

				latest_past_event[0].reminded_next = True
				latest_past_event[0].save()

				for user in User.objects.all():
					if user.active:
						body = settings.EMAIL_REMINDER_BODY
						body = body.replace("<User Name>", user.name)
						body = body.replace("<Next Name>", users[0].name)
						body = body.replace("<Event Date>", latest_past_event[0].date.astimezone(timezone.get_default_timezone()).strftime("%d.%m.%Y"))
						body = body.replace("<Event Time>", latest_past_event[0].date.astimezone(timezone.get_default_timezone()).strftime("%H:%M"))
						body = body.replace("<Add Link>", settings.WWEMS_URL+"/event/add/")
						try:
							send_mail(settings.EMAIL_REMINDER_SUBJECT, body, settings.EMAIL_FROM, [user.email], fail_silently=True)
						except:
							# TODO: Log the error or something?
							pass

			if (latest_past_event[0].date + timedelta(hours=1)) <= timezone.now() and latest_past_event[0].reminded_rate == False:

				self.stdout.write("Last event was " + latest_past_event[0].date.astimezone(timezone.get_default_timezone()).strftime("%d.%m.%Y %H:%M") + ". Rating not reminded! Reminding now.")
				latest_past_event[0].reminded_rate = True
				latest_past_event[0].save()

				for participant in EventParticipant.objects.filter(event=latest_past_event[0]):
					if participant.user.active:
						body = settings.EMAIL_RATING_BODY
						body = body.replace("<User Name>", participant.user.name)
						body = body.replace("<Host Name>", latest_past_event[0].host.name)
						body = body.replace("<Event Link>", settings.WWEMS_URL+"/event/"+str(latest_past_event[0].id)+"/")
						try:
							send_mail(settings.EMAIL_RATING_SUBJECT, body, settings.EMAIL_FROM, [participant.user.email], fail_silently=True)
						except:
							# TODO: Log the error or something?
							pass
