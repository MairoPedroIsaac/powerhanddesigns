# production_settings.py
from .settings import *

# Override settings for production
DEBUG = False
ALLOWED_HOSTS = ['powerhanddesigns.onrender.com', '.onrender.com']

# Add whitenoise for production only
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Use environment variables for security
import os
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')