#!/usr/bin/env python
# encoding: utf-8
"""
googleauth/__init__.py

Created by Axel Schlüter on 2009-12
Copyright (c) 2009, 2010 HUDORA GmbH. All rights reserved.

To use it configuration in settings.py should look like this (this is also in global_django_settings):

GOOGLE_APPS_DOMAIN = 'hudora.de'
GOOGLE_APPS_CONSUMER_KEY = 'hudora.de'
GOOGLE_APPS_CONSUMER_SECRET = '*sekret*'
GOOGLE_API_SCOPE = 'http://www.google.com/m8/feeds/+http://docs.google.com/feeds/+http://spreadsheets.google.com/feeds/'

You also have to set the domain where your application is running
GOOGLE_OPENID_REALM = 'http://*.hudora.biz/'

Then you have to tell where various views live.
LOGIN_REDIRECT_URL = '/admin'

To activate the whole thing set the appropriate Authentication backend and include a callback view.

settings.py:
    AUTHENTICATION_BACKENDS = ('googleappsauth.backends.GoogleAuthBackend',)
urls.py:
    (r'^callback_googleappsauth/', 'googleappsauth.views.callback'),


Using a special middleware you can block access to a compete site.

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'hudoratools.googleauth.middleware.GoogleAuthMiddleware',
)

In addition you can set AUTH_PROTECTED_AREAS to authenticate only access to certain parts of a site, e.g.

AUTH_PROTECTED_AREAS = ['/admin']
"""
