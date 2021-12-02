"""
Django settings for WeissWurstTool project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import environ
env = environ.Env(
	# set casting, default value
	DEBUG=(bool, False),
	WWEMS_URL=(str, "localhost"),
	USE_X_FORWARDED_HOST=(bool, False),
	EMAIL_HOST=(str, None),
	EMAIL_PORT=(int, None),
	EMAIL_FROM=(str, None),
	EMAIL_HOST_USER=(str, None),
	EMAIL_HOST_PASSWORD=(str, None),
	EMAIL_USE_TLS=(bool, False),
	EMAIL_USE_SSL=(bool, False),
	EMAIL_TIMEOUT=(int, None),	
	EMAIL_SSL_KEYFILE=(str, None),
	EMAIL_SSL_CERTFILE=(str, None),
)

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')

WWEMS_URL = env('WWEMS_URL')
USE_X_FORWARDED_HOST = env('USE_X_FORWARDED_HOST')

from urllib.parse import urlparse
domain = urlparse(WWEMS_URL).netloc
ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '[::1]', domain]

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_FROM = env('EMAIL_FROM')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_USE_SSL = env('EMAIL_USE_SSL')
EMAIL_TIMEOUT = env('EMAIL_TIMEOUT')
EMAIL_SSL_KEYFILE = env('EMAIL_SSL_KEYFILE')
EMAIL_SSL_CERTFILE = env('EMAIL_SSL_CERTFILE')


# Application definition

INSTALLED_APPS = [
	'WWEvents.apps.WweventsConfig',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WeissWurstTool.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'WeissWurstTool.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db/db.sqlite3'),
	}
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'de'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
if not DEBUG:
	STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"


# GLOBAL WW-TOOL settings
EMAIL_NEW_EVENT_SUBJECT = 'Ein neuer Weißwurst-Event wurde erstellt!'
EMAIL_NEW_EVENT_BODY = """Hallo <User Name>,

<Host Name> hat soeben ein neues Weißwurst-Event erstellt. Der Wurstgenuss soll am <Event Date> um <Event Time> Uhr in Raum "<Event Room>" stattfinden.
Um dich, oder jemand anderen anzumelden, klicke bitte hier: <Event Link>

Senf-verzierte Grüße
Das Weißwurst-Event Management System
"""
EMAIL_MOD_EVENT_SUBJECT = 'Ein Weißwurst-Event wurde bearbeitet.'
EMAIL_MOD_EVENT_BODY = """Hallo <User Name>,

<Host Name> hat soeben einen aktuellen Weißwurst-Event bearbeitet. Der Wurstgenuss soll nun am <Event Date> um <Event Time> Uhr in Raum "<Event Room>" stattfinden.
Um dich, oder jemand anderen an- oder abzumelden, klicke bitte hier: <Event Link>

Senf-verzierte Grüße
Das Weißwurst-Event Management System
"""
EMAIL_REMINDER_SUBJECT = 'Wir brauchen einen Weißwurst-Host!'
EMAIL_REMINDER_BODY = """Hallo <User Name>,

der letzte Weißwurst-Event war am <Event Date> um <Event Time> Uhr. Das ist nun knapp sechs Tage her!
Laut meiner Datenbank ist <Next Name> als nächster mit Hosten an der Reihe, sollte er verfügbar sein.

Um einen neuen Event anzulegen (mit dir, oder jemand anderes als Host), klicke bitte hier: <Add Link>

Senf-verzierte Grüße
Das Weißwurst-Event Management System
"""
EMAIL_RATING_SUBJECT = 'Bitte bewerte das Weißwurst-Event!'
EMAIL_RATING_BODY = """Hallo <User Name>,

das soeben vergangene Weißwurst-Event war mit Sicherheit ein Genuss. Oder?
Um die Qualität der Würste, der Bretzen, des Senfes und der Organisation in Zukunft verbessern zu können, kannst du eine Bewertung für <Host Name> abgeben.

Klicke dazu bitte hier: <Event Link>

Senf-verzierte Grüße
Das Weißwurst-Event Management System
"""
ICS_TEMPLATE = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:<WW Link>
METHOD:PUBLISH
BEGIN:VEVENT
ORGANIZER;CN="<Host Name>":MAILTO:<Host Mail>
LOCATION:<Event Room>
SUMMARY:WW-Event: <Host Name>
STATUS:CONFIRMED
DESCRIPTION:Ein weiterer Weißwurst Event, geplant vom Weißwurst-Event Management System.\\nUm teilzunehmen, klicke bitte hier: <Event Link>
CLASS:PUBLIC
DTSTART;TZID=<Time Zone>:<Start Date>
DTEND;TZID=<Time Zone>:<End Date>
DTSTAMP;TZID=<Time Zone>:<Now Date>
END:VEVENT
END:VCALENDAR"""