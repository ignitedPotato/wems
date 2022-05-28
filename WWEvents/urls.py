from django.urls import path

from . import views

urlpatterns = [
	path(r'', views.index, name='index'),
	path(r'event/<int:event_id>/', views.details, name="details"),
	path(r'event/<int:event_id>/join/', views.addparticipant, name="addparticipant"),
	path(r'event/<int:event_id>/leave/', views.removeparticipant, name="removeparticipant"),
	path(r'event/<int:event_id>/rate/', views.rateevent, name="rateevent"),
	path(r'event/<int:event_id>/print/', views.printevent, name="printevent"),
	path(r'event/<int:event_id>/edit/', views.editevent, name="editevent"),
	path(r'event/add/', views.addevent, name="addevent"),
	path(r'stats/<int:page>/', views.stats, name="stats"),
	path(r'docs/', views.docs, name="docs"),
	path(r'users/', views.allusers, name="allusers"),
	path(r'event/<int:event_id>/ics/', views.ics, name="ics"),
]
