from .base import *

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

SECRET_KEY = "g_-ipa)6_5+zgug=$u!gbmk#bi(6p=r2xjukh6h2p&3kt$%^w%"

DEBUG = False
ROOT_URLCONF = 'api.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DATABASE', 'partydb'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'admin'),
        'HOST': os.environ.get('POSTGRES_HOST', ''),
        'PORT': os.environ.get('POSTGRES_PORT', ''),
    }
}

ALLOWED_HOSTS = [
    '.vercel.app'
]

CSRF_TRUSTED_ORIGINS = ['https://party-utility.vercel.app']

# Lockdown settings
# INSTALLED_APPS += [
#     'lockdown',
# ]

# MIDDLEWARE += [
#     'lockdown.middleware.LockdownMiddleware',
# ]

# LOCKDOWN_ENABLED = False
# LOCKDOWN_PASSWORDS = ('2023novapumpkin2023',)
# LOCKDOWN_AUTHFORM_STAFF_ONLY = False
# LOCKDOWN_URL_EXCEPTIONS = [
#     r'^/static/*',   # unlock /static/*
#     r'^/robots.txt$',
# ]

# Sentry initialization.
# sentry_sdk.init(
#     dsn="https://__redcated__.ingest.sentry.io/__redacted2__",
#     environment="prod",
#     integrations=[DjangoIntegration()]
# )

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# Prod Security Settings

# If set to a non-zero integer value, the SecurityMiddleware sets the HTTP Strict Transport Security header on all
# responses that do not already have it.
SECURE_HSTS_SECONDS = 60  # Set this to something higher later e.g. 2592000 if everything works in prod

# If True, the SecurityMiddleware redirects all non-HTTPS requests to HTTPS (except for those URLs matching a regular
# expression listed in SECURE_REDIRECT_EXEMPT).
SECURE_SSL_REDIRECT = True

# Whether to use a secure cookie for the session cookie. If this is set to True, the cookie will be marked as “secure”,
# which means browsers may ensure that the cookie is only sent under an HTTPS connection.
SESSION_COOKIE_SECURE = True

# Whether to use a secure cookie for the CSRF cookie. If this is set to True, the cookie will be marked as “secure”,
# which means browsers may ensure that the cookie is only sent with an HTTPS connection.
CSRF_COOKIE_SECURE = True

# If True, the SecurityMiddleware adds the includeSubDomains directive to the HTTP Strict Transport Security header.
# It has no effect unless SECURE_HSTS_SECONDS is set to a non-zero value.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# If True, the SecurityMiddleware adds the preload directive to the HTTP Strict Transport Security header.
# It has no effect unless SECURE_HSTS_SECONDS is set to a non-zero value.
SECURE_HSTS_PRELOAD = True

# will be notified of 500 errors by email.
ADMINS = [
    ("Solomon Rodrigues", "solomonrodrigues@hotmail.com")
]

# will be notified of 404 errors. IGNORABLE_404_URLS can help filter out spurious reports.
MANAGERS = [
    ("Solomon Rodrigues", "solomonrodrigues@hotmail.com")
]

IGNORABLE_404_URLS = []

STATIC_URL = '/static/'

# Include the path to the 'static' directory within the 'partyutility' app
STATICFILES_DIRS = [
    BASE_DIR / 'partyutility' / 'static',
]

# Specify the directory where 'collectstatic' will gather static files for deployment
STATIC_ROOT = BASE_DIR / 'staticfiles_build' / 'static'

# Whitenoise settings
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
