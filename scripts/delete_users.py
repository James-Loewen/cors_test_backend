#!/home/pynoodler/.virtualenvs/cors_venv/bin/python

import sys
import os
from pathlib import Path

try:
    import django
    from django.contrib.auth.models import User
    from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
except ImportError:
    sys.exit("Django is not installed.")

# DJANGO PROJECT SETUP
path = Path(__file__).resolve().parent.parent
sys.path.append(path.as_posix())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cors_test_backend.settings")

try:
    django.setup()
except ImproperlyConfigured:
    sys.exit("Django settings are incorrect or not found.")

# SCRIPT START
try:
    all_non_su = User.objects.filter(is_superuser=False)
    all_non_su.delete()
except ObjectDoesNotExist:
    print("No non-superuser users found.")
