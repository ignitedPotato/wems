from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.utils import dateparse
from datetime import datetime, timedelta
from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import *

def index(request):
	latest_event_list = Event.objects.order_by('-date')[:4]
	user_list = sorted(User.objects.all(),  key=lambda m: m.get_user_standing)[:5]

	context = {'latest_event_list': latest_event_list, 'user_list': user_list}
	return render(request, 'index.html', context)

def details(request, event_id):
	try:
		event = Event.objects.get(id=event_id)
	except Exception as err:
		raise err
	pform = ParticipantForm()
	rform = RatingForm()
	context = {'event': event, "pform": pform, "rform": rform}
	return render(request, 'details.html', context)

def addparticipant(request, event_id):
	if request.method == 'POST':
		form = ParticipantForm(request.POST)
		if form.is_valid():
			try:
				p = form.save(commit=False)
				event = Event.objects.get(id=event_id)
				p.event = event
				p.save()
			except Exception as err:
				raise err
	return HttpResponseRedirect("/event/"+str(event_id)+"/")

def removeparticipant(request, event_id):
	if request.method == 'POST':
		try:
			event = Event.objects.get(id=event_id)
			participant = request.POST['participant']

			p = EventParticipant.objects.get(id=participant)
			p.delete()
		except Exception as err:
			raise err
	return HttpResponseRedirect("/event/"+str(event_id)+"/")

def rateevent(request, event_id):
	if request.method == 'POST':
		form = RatingForm(request.POST)
		if form.is_valid():
			try:
				r = form.save(commit=False)
				event = Event.objects.get(id=event_id)
				if event.is_past:
					r.event = event
					r.save()
			except Exception as err:
				raise err
	return HttpResponseRedirect("/event/"+str(event_id)+"/")

def printevent(request, event_id):
	try:
		event = Event.objects.get(id=event_id)
		context = {'event': event}
		return render(request, 'print.html', context)
	except Exception as err:
		raise err

def addevent(request):
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			e = form.save()

			# Send mail to all if event is in the future
			if not e.is_past:
				for user in User.objects.all():
					if user.active and user.id != e.host.id:
						body = settings.EMAIL_NEW_EVENT_BODY
						body = body.replace("<User Name>", user.name)
						body = body.replace("<Host Name>", e.host.name)
						body = body.replace("<Event Date>", e.date.astimezone(timezone.get_default_timezone()).strftime("%d.%m.%Y"))
						body = body.replace("<Event Time>", e.date.astimezone(timezone.get_default_timezone()).strftime("%H:%M"))
						body = body.replace("<Event Room>", e.room.name)
						body = body.replace("<Event Link>", settings.WWEMS_URL+"/event/"+str(e.id)+"/")
						try:
							email = EmailMessage(settings.EMAIL_NEW_EVENT_SUBJECT, body, settings.EMAIL_FROM, [user.email])
							email.attach('ww-event-'+ str(e.id) +'.ics', e.get_ics(), 'text/calendar')
							email.send()
						except:
							# TODO: Log the error or something?
							pass
			return HttpResponseRedirect("/event/"+str(e.id)+"/")

	else:
		form = EventForm()

	context = {"form": form}
	return render(request, 'addevent.html', context)

def editevent(request, event_id):
	if request.method == 'POST':
		try:
			old_e = Event.objects.get(id=event_id)
		except Exception as err:
			raise err
		form = EventForm(request.POST, instance=old_e)
		if form.is_valid():
			e = form.save()

			# Send mail to all if event is in the future
			if not e.is_past:
				for user in User.objects.all():
					if user.active and user.id != e.host.id:
						body = settings.EMAIL_NEW_EVENT_BODY
						body = body.replace("<User Name>", user.name)
						body = body.replace("<Host Name>", e.host.name)
						body = body.replace("<Event Date>", e.date.astimezone(timezone.get_default_timezone()).strftime("%d.%m.%Y"))
						body = body.replace("<Event Time>", e.date.astimezone(timezone.get_default_timezone()).strftime("%H:%M"))
						body = body.replace("<Event Room>", e.get_room_display())
						body = body.replace("<Event Link>", settings.WWEMS_URL+"/event/"+str(e.id)+"/")
						try:
							email = EmailMessage(settings.EMAIL_NEW_EVENT_SUBJECT, body, settings.EMAIL_FROM, [user.email])
							email.attach('ww-event-'+ str(e.id) +'.ics', e.get_ics(), 'text/calendar')
							email.send()
						except:
							# TODO: Log the error or something?
							pass
			return HttpResponseRedirect("/event/"+str(e.id)+"/")

	else:
		try:
			e = Event.objects.get(id=event_id)
		except Exception as err:
			raise err
		form = EventForm(instance=e)
	
	context = {"form": form}
	return render(request, 'addevent.html', context)


def stats(request, page):
	if page == None or int(page) < 1:
		page = 1
	else:
		page = int(page)

	num_pages = range(1, int(Event.objects.count()/10) +2)
	if page not in num_pages:
		page = 1

	event_list = Event.objects.order_by('-date')[(page*10)-10:page*10]

	if page == 1:
		user_host_counts = Event.objects.values('host').annotate(models.Count('id'))
		user_host_counts = sorted(user_host_counts,  key=lambda m: m['id__count'], reverse=True)[:5]
		for host in user_host_counts:
			host['host'] = User.objects.filter(id=host['host'])[0]
		context = {'event_list': event_list, 'num_pages': num_pages, 'curr_page': page, 'user_host_counts' : user_host_counts}
	else:
		context = {'event_list': event_list, 'num_pages': num_pages, 'curr_page': page}

	return render(request, 'stats.html', context)

def docs(request):
	context = {}
	return render(request, 'docs.html', context)

def allusers(request):
	user_list = sorted(User.objects.all(),  key=lambda m: m.get_user_standing)
	context = {'user_list': user_list}
	return render(request, 'allusers.html', context)

def ics(request, event_id):
	try:
		event = Event.objects.get(id=event_id)
		response = HttpResponse(event.get_ics(), content_type="text/calendar")
		response['Content-Disposition'] = 'attachment; filename="ww-event-'+ str(event.id) +'.ics"'
		return response
	except Exception as err:
		raise err
