#!/usr/bin/env python
# encoding: utf-8
"""
googleauth/middleware.py - force Google Apps Authentication for the whole site.

Created by Axel Schlüter on 2009-12
Copyright (c) 2009, 2010 HUDORA GmbH. All rights reserved.
"""

from django.conf import settings
from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
import django.contrib.auth as djauth
import googleappsauth.views


class GoogleAuthMiddleware(object):
    """Force Google Apps Authentication for the whole site.
    
    Using settings.AUTH_PROTECTED_AREAS you can restrict authentication 
    o only parts of a site.
    """
    
    def process_request(self, request):
        # zuerst ueberpruefen wir, ob wir fuer die aktuelle URL 
        # ueberhaupt einen gueltigen User einloggen muessen
        path = request.META['PATH_INFO']
        areas = getattr(settings, 'AUTH_PROTECTED_AREAS', [])
        # LEGACY: AUTH_PROTECTED_AREAS = "foo+bar" - to removed in Version 2.9
        if hasattr(areas, 'split'):
            areas = areas.split('+')
        matches = [area for area in areas if path.startswith(area)]
        if len(matches) == 0:
            return
        
        # Dont force authentication for the callback URL since it would
        # result in a loop
        callback_url = request.build_absolute_uri(reverse(googleappsauth.views.callback))
        if callback_url.endswith(path):
            return
        
        # ok, die Seite muss auth'd werden. Haben wir vielleicht
        # schon einen geauth'd User in der aktuellen Session? 
        if request.user.is_authenticated():
            return
        
        # nein, wir haben noch keinen User. Also den Login ueber
        # Google Apps OpenID/OAuth starten und Parameter in Session speichern
        return googleappsauth.views.login(request,
            redirect_url="%s?%s" % (path, request.META.get('QUERY_STRING', '')))
