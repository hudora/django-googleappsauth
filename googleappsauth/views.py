#!/usr/bin/env python
# encoding: utf-8
"""
googleappsauth/views.py - 

Created by Axel Schlüter on 2009-12
Copyright (c) 2009, 2010 HUDORA GmbH. All rights reserved.
"""

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponse, HttpResponseRedirect, Http404
import django.contrib.auth as djauth
import googleappsauth.openid


_google_apps_domain = getattr(settings, 'GOOGLE_APPS_DOMAIN', None)
_google_openid_endpoint = getattr(settings, 'GOOGLE_OPENID_ENDPOINT', None)
_google_openid_realm = getattr(settings, 'GOOGLE_OPENID_REALM', None)
_oauth_consumer_key = getattr(settings, 'GOOGLE_APPS_CONSUMER_KEY', None)
_oauth_consumer_secret = getattr(settings, 'GOOGLE_APPS_CONSUMER_SECRET', None)
_google_api_scope = getattr(settings, 'GOOGLE_API_SCOPE', None)


def login(request, redirect_field_name=REDIRECT_FIELD_NAME, redirect_url=None):
    # zuerst bestimmen wir, wohin nach erfolgtem Login in die App
    # umgeleitet werden soll
    if not redirect_url:
        redirect_url = request.REQUEST.get(redirect_field_name)
        if not redirect_url:
            redirect_url =  getattr(settings, 'LOGIN_REDIRECT_URL', '/')
    request.session['redirect_url'] = redirect_url

    # jetzt bauen wir uns die URL fuer den Callback zusammen, unter
    # dem wir von Google aufgerufen werden moechten nach dem Login
    callback_url = request.build_absolute_uri(reverse(callback))
    request.session['callback_url'] = callback_url

    # und schliesslich konstruieren wir darauf die Google-OpenID-
    # Endpoint-URL, auf die wir dann den Benutzer umleiten
    url = googleappsauth.openid.build_login_url(
            _google_openid_endpoint, _google_openid_realm,
            callback_url, _oauth_consumer_key, _google_api_scope)
    return HttpResponseRedirect(url)


def callback(request):
    # haben wir einen erfolgreichen Login? Wenn nicht gehen wir
    # sofort zurueck, ohne einen Benutzer einzuloggen
    callback_url = request.session.get('callback_url', '/')
    identifier = googleappsauth.openid.parse_login_response(request, callback_url)
    if not identifier:
        # TODO: was ist hier los?
        return HttpResponseRedirect('/')
    
    # jetzt holen wir uns die restlichen Daten aus dem Login
    attributes = {
        'email': googleappsauth.openid.get_email(request),
        'language': googleappsauth.openid.get_language(request),
        'firstname': googleappsauth.openid.get_firstname(request),
        'lastname': googleappsauth.openid.get_lastname(request)}
    
    # wenn wir ein OAuth request token bekommen haben machen wir
    # daraus jetzt noch flott ein access token
    request_token = googleappsauth.openid.get_oauth_request_token(request)
    #if request_token:
    #    attributes['access_token'] = None
    #    raise Exception('access token handling not yet implemented!')
    
    # Usernames are based on E-Mail Addresses which are unique.
    username = attributes.get('email', identifier).split('@')[0].replace('.', '')
    
    # schliesslich melden wir den Benutzer mit seinen Attributen am
    # Auth-System von Django an, dann zurueck zur eigentlichen App
    user = djauth.authenticate(identifier=username, attributes=attributes)
    if not user:
        # For some reason I do not fully understand we get back a "None"" coasionalty - retry.
        user = djauth.authenticate(identifier=username, attributes=attributes)
        if not user:
            # die Authentifizierung ist gescheitert
            raise RuntimeError("Authentifizierungsproblem: %s|%s|%s" % (username, identifier, attributes))
    djauth.login(request, user)
    redirect_url = request.session['redirect_url']
    # del request.session['redirect_url']
    return HttpResponseRedirect(redirect_url)


def logout(request):
    djauth.logout(request)
    return HttpResponseRedirect('https://www.google.com/a/%s/Logout' % _google_apps_domain)
