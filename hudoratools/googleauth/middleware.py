from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
import django.contrib.auth as djauth
import views


class GoogleAuthMiddleware(object):
    def process_request(self, request):
        # zuerst ueberpruefen wir, ob wir fuer die aktuelle URL 
        # ueberhaupt einen gueltigen User einloggen muessen
        path = request.META['PATH_INFO']
        areas = getattr(settings, 'AUTH_PROTECTED_AREAS','').split('+')
        matches = filter(lambda area: path.startswith(area), areas)
        if len(matches) == 0:
            return

        # ok, die Seite muss auth'd werden. Haben wir vielleicht
        # schon einen geauth'd User in der aktuellen Session? 
        if request.user.is_authenticated():
            return

        # nein, wir haben noch keinen User. Also den Login ueber
        # Google Apps OpenID/ OAuth starten
        return views.login(request, redirect_url=path)
