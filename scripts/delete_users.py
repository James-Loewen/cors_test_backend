#!/home/pynoodler/.virtualenvs/cors_venv/bin/python

import sys
import os
from pathlib import Path

try:
    import django
    from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
except ImportError:
    sys.exit("Django is not installed.")

# DJANGO PROJECT SETUP
path = Path(__file__).resolve().parent.parent
sys.path.append(path.as_posix())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cors_test_backend.settings")

try:
    django.setup()
    from django.contrib.auth.models import User
except ImproperlyConfigured:
    sys.exit("Django settings are improperly configured.")
except Exception as e:
    sys.exit(f"Something went wrong. Error: {e}")

# SCRIPT START
all_non_su = User.objects.filter(is_superuser=False)
num_users = len(all_non_su)
if num_users > 0:
    all_non_su.delete()
    print(f"{num_users} user(s) deleted.")
else:
    print("No non-superuser users found.")
