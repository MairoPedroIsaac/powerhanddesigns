#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input

# Create superusers if they don't exist
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
import os
User = get_user_model()

# Create ADMIN superuser
if not User.objects.filter(username=os.environ.get('DJANGO_SUPERUSER_USERNAME')).exists():
    User.objects.create_superuser(
        username=os.environ.get('DJANGO_SUPERUSER_USERNAME'),
        email=os.environ.get('DJANGO_SUPERUSER_EMAIL'),
        password=os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    )
    print("ADMIN superuser created!")
else:
    print("ADMIN superuser already exists.")

# Create powerhanddesigns superuser
if not User.objects.filter(username=os.environ.get('DJANGO_SUPERUSER_USERNAME2')).exists():
    User.objects.create_superuser(
        username=os.environ.get('DJANGO_SUPERUSER_USERNAME2'),
        email=os.environ.get('DJANGO_SUPERUSER_EMAIL2'),
        password=os.environ.get('DJANGO_SUPERUSER_PASSWORD2')
    )
    print("powerhanddesigns superuser created!")
else:
    print("powerhanddesigns superuser already exists.")
EOF