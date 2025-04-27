"""
WSGI config for expensetracker_enhanced project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expensetracker_enhanced.settings')

# Get WSGI application
application = get_wsgi_application()

# Add WhiteNoise middleware for serving static files
application = WhiteNoise(application, root=settings.STATIC_ROOT)

# Configure WhiteNoise compression and caching
application.add_files(settings.STATIC_ROOT, prefix='static/')
if not settings.DEBUG:
    application.add_cache_headers = True
    application.compression_enabled = True
    # Set maximum age for cached files (30 days)
    application.max_age = 2592000

    # Enable Brotli compression if available
    application.use_brotli = True
    
    # Add security headers
    application.add_headers_function = lambda headers: headers.update({
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block'
    })
