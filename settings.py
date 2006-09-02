# -*- coding: utf-8 -*-
"""
TESTING SETTINGS for django.

Copyright (c) HUDORA. All rights reserved.
"""

# See http://docs.djangoproject.com/en/dev/ref/settings/ for inspiration

import os
import django

# calculated paths for django and the site
# used as starting points for various other paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = True
TEMPLATE_STRING_IF_INVALID = "_#_%s_#_"
DEBUG_PROPAGATE_EXCEPTIONS = True

MEDIA_URL = 'http://s.hdimg.net/huLOG/'

# for testing
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(SITE_ROOT, 'test.db')

ROOT_URLCONF = 'huLOG.urls'
SITE_ID = 1 # intern.hudora.biz

INSTALLED_APPS = (
    'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.sites',
    'django.contrib.admin', 'django.contrib.comments', 'django.contrib.markup',
    #'debug_toolbar',
    'hudoratools',
)

TEMPLATE_DIRS = (os.path.join(SITE_ROOT, 'generic_templates'))

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.core.context_processors.auth', 'django.core.context_processors.debug',
  'django.core.context_processors.i18n', 'django.core.context_processors.media',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'hudjango.middleware.clienttrack.ClientTrackMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)


# This example is all working panels, not all are active with default settings
# DEBUG_TOOLBAR_PANELS = (
#     'debug_toolbar.panels.sql.SQLDebugPanel',
#     'debug_toolbar.panels.headers.HeaderDebugPanel',
#     'debug_toolbar.panels.cache.CacheDebugPanel',
#     'debug_toolbar.panels.profiler.ProfilerDebugPanel',
#     'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#     'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#     'debug_toolbar.panels.templates.TemplatesDebugPanel',
#     # If you are using the profiler panel you don't need the timer
#     # 'debug_toolbar.panels.timer.TimerDebugPanel',
# )

ADMIN_MEDIA_PREFIX = 'http://s.hdimg.net/djangoadmin/1.0.2/'
INTERNAL_IPS = ('127.0.0.1')
TIME_FORMAT = 'H:i'
TIME_ZONE = 'Europe/Amsterdam'
DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'
USE_I18N = True
LANGUAGE_CODE = 'de-de'
LANGUAGES = (
  ('zh', 'Chinese'),
  ('de', 'German'),
  ('en', 'English'),
)

SECRET_KEY = 'sua1+khy2x-dojd_+r2j^7$asdfasQ@#$)!v94tpxe-g&_n6xxxv0!f+y'
CACHE_BACKEND = 'memcached://balancer.local.hudora.biz:11211/'
os.environ['PYJASPER_SERVLET_URL'] = 'http://jasper.local.hudora.biz:8080/pyJasper/jasper.py'
COUCHDB_STORAGE_OPTIONS = {'server': "http://couchdb1.local.hudora.biz:5984"}
PREPEND_WWW = False
