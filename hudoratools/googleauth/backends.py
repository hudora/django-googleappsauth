from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, SiteProfileNotAvailable
from datetime import datetime
import re


class GoogleAuthBackend:
    def authenticate(self, identifier=None, attributes=None):
        # da wir von Google keinen Benutzernamen bekommen versuchen wir zuerst, 
        # den ersten Teil der Emailadresse zu nehmen. Wenn wir keine Email haben 
        # dann bleibt nur der OpenID-Identifier als Benutzername
        email = attributes.get('email')
        username = identifier
        if email:
            parts=re.findall(r'([a-zA-Z0-9._%+-]+)@',email)
            if len(parts) == 1:
                username = parts[0]

        # zuerst holen wir uns den passenden Benutzer aus der Datenbank bzw. 
        # legen einen neuen Benutzer an. 
        user, created = User.objects.get_or_create(username=username)
        if created:
            # fuer einen neuen Benutzer erzeugen wir hier ein Zufallspasswort,
            # sodass er sich nicht mehr anders als ueber Google Apps einloggen kann
            passwd = User.objects.make_random_password()
            user.username = username
            user.set_password(passwd)

        # jetzt aktualisieren wir die Attribute des Benutzers mit den neuesten 
        # Werten von Google, falls sich da was geaendert haben sollte
        user.first_name = attributes.get('firstname')
        user.last_name = attributes.get('lastname')
        user.email = attributes.get('email')
        user.save()

        # schliesslich speichern wir das Access Token des Benutzers in seinem
        # User Profile.
        try:
            profile = self._get_or_create_user_profile(user)
            profile.language = attributes.get('language')
            profile.access_token = attributes.get('access_token','')
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
