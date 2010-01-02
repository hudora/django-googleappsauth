#!/usr/bin/env python
# encoding: utf-8
"""
googleauth/tools.py - 

Created by Axel Schlüter on 2009-12
Copyright (c) 2009 HUDORA GmbH. All rights reserved.
"""

import oauth
import httplib
import random
from django.conf import settings


""" Google OAuth Key und Secret, wird im Backend fuer hudora.de konfiguriert """
_apps_domain = getattr(settings, 'GOOGLE_APPS_DOMAIN', None)
_consumer_key = getattr(settings, 'GOOGLE_APPS_CONSUMER_KEY', None)
_consumer_secret = getattr(settings, 'GOOGLE_APPS_CONSUMER_SECRET', None)


""" Google OAuth URLs, auf die zugegriffen werden soll """
SERVER = 'www.google.com'
REQUEST_TOKEN_URL = 'https://%s/accounts/OAuthGetRequestToken' % SERVER
AUTHORIZATION_URL = 'https://%s/accounts/OAuthAuthorizeToken' % SERVER
ACCESS_TOKEN_URL = 'https://%s/accounts/OAuthGetAccessToken' % SERVER
PROFILES_URL = 'http://%s/m8/feeds/profiles/domain/%s/full/' % (SERVER, _apps_domain)


""" die globalen Objekte zum Zugriff auf Google OAuth """
_consumer = oauth.OAuthConsumer(_consumer_key, _consumer_secret)
_connection = httplib.HTTPSConnection(SERVER)
_signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()


def fetch_response(req, conn):
    """
    helper method, fuehrt einen HTTP-Request durch und liefert die 
    vom Server gelieferte Antwort als String zurueck.
    """
    conn.request(req.http_method, req.to_url())
    resp = conn.getresponse()
    return resp.read()


def token_from_session(request, attribute_name='access_token'):
    """
    helper method, liesst das serialisierte Access Token aus der 
    Session und erzeugt wieder ein Object daraus.
    """
    token_str = request.session.get(attribute_name, None)
    if not token_str:
        return None
    return token_from_string(token_str)


def token_from_string(serialized_token):
    """
    helper method, konvertiert ein als String serialisiertes 
    Token wieder zurueck in ein Python Object 
    """
    token = oauth.OAuthToken.from_string(serialized_token)
    return token


def get_request_token(callback_url, google_scope):
    """
    OAuth call, laedt ein neuen Request-Token vom Server 
    """
    req = oauth.OAuthRequest.from_consumer_and_token(_consumer,
        http_url=REQUEST_TOKEN_URL,
        parameters={'scope': google_scope,
                    'oauth_callback': callback_url})
    req.sign_request(_signature_method, _consumer, None)
    resp = fetch_response(req, _connection)
    req_token = oauth.OAuthToken.from_string(resp)
    return req_token


def get_access_token(req_token, verifier=None):
    """
    OAuth call, laedt nach erfolgtem Auth des Users und 
    der App das eigentliche Access-Token von Google. Mit diesem
    Token koennen dann die Calls durchgefuehrt werden, fuer die 
    bei Google ein vorheriges Auth notwendig ist.
    """
    parameters={}
    if verifier:
        parameters['oauth_verifier'] = verifier

    req = oauth.OAuthRequest.from_consumer_and_token(_consumer, token=req_token,
        http_url=ACCESS_TOKEN_URL, parameters=parameters)
    req.sign_request(_signature_method, _consumer, req_token)
    resp = fetch_response(req, _connection)
    access_token = oauth.OAuthToken.from_string(resp) 
    return access_token


def build_auth_url(req_token):
    """
    OAuth call, erzeugt aus dem vorher geladenen Request-Token 
    die URL, auf die der Benutzer zu Google umgeleitet werden muss. Dort
    authorisiert der Benutzer dann zuerst sich selbst und in der Folge unsere 
    App zum Zugriff auf das API. Nach erfolgtem Auth leitet Google den Benutzer
    auf die bei Google hinterlegte URL zurueck zur App, es muss als der 
    richtige Key genutzt werden, damit der Redirect wirklich auf unseren 
    Server geht.
    """

    req = oauth.OAuthRequest.from_consumer_and_token(_consumer, token=req_token,
        http_url=AUTHORIZATION_URL,
        parameters={'hd': 'hudora.de'})
    req.sign_request(_signature_method, _consumer, req_token)
    auth_url = req.to_url()
    return auth_url


def get_user_profile(access_token, username):
    req = oauth.OAuthRequest.from_consumer_and_token(_consumer, token=access_token,
        http_method='GET',
        http_url=PROFILES_URL + username,
        parameters={'v': '3.0'})
    req.sign_request(_signature_method, _consumer, access_token)
    resp = fetch_response(req, _connection)
    return 'schluete'



# OpenID
# https://www.google.com/accounts/o8/site-xrds?hd=hudora.de
# user's login identifier, as openid.claimed_id
# requested user attributes, as openid.ax.value.email (if requested)
# authorized OAuth request token, as openid.ext2.request_token (if requested)
