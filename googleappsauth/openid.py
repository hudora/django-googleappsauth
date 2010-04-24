#!/usr/bin/env python
# encoding: utf-8
"""
googleauth/tools.py - 

Created by Axel Schlüter on 2009-12
Copyright (c) 2009 HUDORA GmbH. All rights reserved.
"""

import re
import urllib


class OpenIdError(Exception):

    def __init__(self, why=None):
        Exception.__init__(self, why)
        self.why = why


def build_login_url(endpoint_url, realm, callback_url, oauth_consumer=None, oauth_scope=None):
    # zuerst ueberpruefen wir, ob die Callback Url gueltig ist
    if not endpoint_url:
        raise OpenIdError('invalid GOOGLE_OPENID_ENDPOINT %r' % endpoint_url)
    if not realm:
        raise OpenIdError('invalid GOOGLE_OPENID_REALM %r' % realm)
    if not callback_url:
        raise OpenIdError('invalid callback url %r' % callback_url)

    # 'openid.mode': 'checkid_setup' oder 'checkid_immediate'
    params = {
        # zuerst die Keys fuer die eigentliche Authentifizierung
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup', 
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.realm': realm,
        'openid.return_to': callback_url,

        # jetzt noch die Keys fuer die 'extended attributes', damit wir den
        # Realnamen und die Emailadresse des eingeloggten Benutzers bekommen
        'openid.ns.ax': 'http://openid.net/srv/ax/1.0',
        'openid.ax.mode': 'fetch_request',
        'openid.ax.required': 'firstname,lastname,language,email',
        'openid.ax.type.email': 'http://axschema.org/contact/email',
        'openid.ax.type.firstname': 'http://axschema.org/namePerson/first',
        'openid.ax.type.language': 'http://axschema.org/pref/language',
        'openid.ax.type.lastname': 'http://axschema.org/namePerson/last',
    }

    # und schliesslich noch die Keys fuer OAuth, damit wir einen 
    # Request Key bekommen, den wir dann auf Wunsch zum Access Key
    # machen koennen (notwendig fuer einen API-Zugriff auf GApps)
    if oauth_consumer and oauth_scope:
        params['openid.ns.oauth']='http://specs.openid.net/extensions/oauth/1.0'
        params['openid.oauth.consumer']=oauth_consumer
        params['openid.oauth.scope']=oauth_scope

    # jetzt bauen wir die Parameter zusammen mit der URL des OpenID-
    # Endpoints noch zu einer kompletten URL zusammen und liefern
    # diese zurueck
    urlencoded_params = urllib.urlencode(params)
    redirect_url = endpoint_url
    if endpoint_url.find('?') == -1:
        redirect_url += '?%s' % urlencoded_params
    else:
        redirect_url += '&%s' % urlencoded_params
    return redirect_url


def parse_login_response(request, callback_url=None):
    # haben wir ueberhaupt eine positive Antwort?
    args = _get_request_args(request)
    is_valid_logon = args.get('openid.mode') == 'id_res'

    # basic checks: stimmen die URLs ueberein?
    if callback_url:
        if callback_url != _lookup_key(args, 'openid.return_to'):
            is_valid_logon = None

    # wir holen uns den OpenID identifier
    identifier = _lookup_key(args, 'openid.identity')
    if identifier == None:
        identifier = _lookup_key(args, 'openid.claimed_id')

    # wenn der Login gueltig war liefern wir jetzt den 
    # OpenID-Identifier zurueck, ansonsten None
    if is_valid_logon:
        return identifier
    else:
        return None


def get_email(request):
    return _lookup_key(_get_request_args(request), 'value.email')


def get_language(request):
    return _lookup_key(_get_request_args(request), 'value.language')


def get_firstname(request):
    return _lookup_key(_get_request_args(request), 'value.firstname')


def get_lastname(request):
    return _lookup_key(_get_request_args(request), 'value.lastname')


def get_oauth_request_token(request):
    return _lookup_key(_get_request_args(request), 'request_token')


def _get_request_args(request):
    args = request.GET
    if request.method == 'POST':
        args = request.POST
    return args


def _lookup_key(args, key_pattern):
    for key, value in args.items():
        if key == key_pattern or re.search(key_pattern, key):
            if isinstance(value, list):
                return value[0]
            else:
                return value
    return None
