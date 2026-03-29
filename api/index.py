import sys
import os

# Add pyservice directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pyservice'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyservice.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel handler
app = application
