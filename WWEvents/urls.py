from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^event/(?P<event_id>[0-9]+)/$', views.details, name="details"),
	url(r'^event/(?P<event_id>[0-9]+)/join/$', views.addparticipant, name="addparticipant"),
	url(r'^event/(?P<event_id>[0-9]+)/leave/$', views.removeparticipant, name="removeparticipant"),
	url(r'^event/(?P<event_id>[0-9]+)/rate/$', views.rateevent, name="rateevent"),
	url(r'^event/(?P<event_id>[0-9]+)/print/$', views.printevent, name="printevent"),
	url(r'^event/(?P<event_id>[0-9]+)/edit/$', views.editevent, name="editevent"),
	url(r'^event/add/$', views.addevent, name="addevent"),
	url(r'^stats/(?P<page>[0-9]+)/$', views.stats, name="stats"),
	url(r'^docs/$', views.docs, name="docs"),
	url(r'^users/$', views.allusers, name="allusers"),
	url(r'^event/(?P<event_id>[0-9]+)/ics/$', views.ics, name="ics"),
]
