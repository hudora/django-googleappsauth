#!/usr/bin/env python
# encoding: utf-8
"""
googleauth/backends.py - Django authentication backend connecting to Google Apps

Created by Axel Schlüter on 2009-12
Copyright (c) 2009 HUDORA GmbH. All rights reserved.
"""

from datetime import datetime
from django.conf import settings
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.contrib.contenttypes.models import ContentType
from django.db import models
import re


class GoogleAuthBackend:

    def authenticate(self, identifier=None, attributes=None):
        # da wir von Google keinen Benutzernamen bekommen versuchen wir zuerst, 
        # den ersten Teil der Emailadresse zu nehmen. Wenn wir keine Email haben 
        # dann bleibt nur der OpenID-Identifier als Benutzername
        email = attributes.get('email', '')
        username = attributes.get('email', identifier).split('@')[0].replace('.', '')
        
        # zuerst holen wir uns den passenden Benutzer aus der Datenbank bzw. 
        # legen einen neuen Benutzer an. 
        user, created = User.objects.get_or_create(email=email)
        if created:
            # fuer einen neuen Benutzer erzeugen wir hier ein Zufallspasswort,
            # sodass er sich nicht mehr anders als ueber Google Apps einloggen kann
            passwd = User.objects.make_random_password()
            user.username = username
            user.set_password(passwd)
            # note creation in log
            LogEntry.objects.log_action(1, ContentType.objects.get_for_model(User).id,
                                    user.id, unicode(User),
                                    ADDITION, "durch googleauth automatisch erzeugt")
            
        # jetzt aktualisieren wir die Attribute des Benutzers mit den neuesten 
        # Werten von Google, falls sich da was geaendert haben sollte
        user.first_name = attributes.get('firstname')
        user.last_name = attributes.get('lastname')
        user.is_staff = True
        user.save()
        
        # schliesslich speichern wir das Access Token des Benutzers in seinem
        # User Profile.
        try:
            profile = self._get_or_create_user_profile(user)
            profile.language = attributes.get('language')
            profile.access_token = attributes.get('access_token', '')
            profile.save()
        except SiteProfileNotAvailable:
            pass
        
        # das war's, Benutzer zurueckliefern, damit ist Login geglueckt
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def _get_or_create_user_profile(self, user):
        profile_module = getattr(settings, 'AUTH_PROFILE_MODULE', False)
        if not profile_module:
            raise SiteProfileNotAvailable
        app_label, model_name = profile_module.split('.')
        model = models.get_model(app_label, model_name)
        try: 
            return user.get_profile()
        except model.DoesNotExist:
            profile = model()
            profile.user = user
            return profile
