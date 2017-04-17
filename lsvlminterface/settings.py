"""
Django settings for lsvlminterface project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e=l43l(%8ah+xoujff_+7=9_gw(x9ets3xzih-z-doinb=9b!e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates/'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corpora',
    'lm',
    'experiments',
    'util',
    'jsonify',
    'mod_wsgi.server',
    'sslserver',
    #'pipeline',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'lsvlminterface.urls'

WSGI_APPLICATION = 'lsvlminterface.wsgi.application'

LOGIN_URL = "login"


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = ( os.path.join(BASE_DIR, 'static'), )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'pipeline.finders.PipelineFinder',
)

try:
    import local_settings
except ImportError as e:
    pass

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

#AUTH_LDAP_START_TLS = True
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0
}

AUTH_LDAP_SERVER_URI = "ldap://tyr.lsv.uni-saarland.de:389"
#AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,cn=users,cn=accounts,dc=lsv,dc=uni-saarland,dc=de"
AUTH_LDAP_BIND_DN = "uid=proxyuser,cn=users,cn=accounts,dc=lsv,dc=uni-saarland,dc=de"
AUTH_LDAP_BIND_PASSWORD = "salamsosis"
AUTH_LDAP_USER_SEARCH  = LDAPSearch( "cn=users,cn=accounts,dc=lsv,dc=uni-saarland,dc=de", ldap.SCOPE_SUBTREE, "(&(uid=%(user)s)(objectClass=posixAccount))")
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("cn=groups,cn=accounts,dc=lsv,dc=uni-saarland,dc=de", ldap.SCOPE_SUBTREE, "(&(member=%(dn)s)(objectClass=groupOfNames))")
AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName", "last_name": "sn", "email" : "mail"}

