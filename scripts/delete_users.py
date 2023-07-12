# DJANGO PROJECT SETUP
import sys
import os
from pathlib import Path

import django

path = Path(__file__).resolve().parent.parent
sys.path.append(path.as_posix())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cors_test_backend.settings")
django.setup()

# SCRIPT START
from django.contrib.auth.models import User

all_non_su = User.objects.filter(is_superuser=False)
all_non_su.delete()
