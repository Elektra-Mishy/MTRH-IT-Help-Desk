#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_data

python manage.py shell << 'EOF'
from django.contrib.sites.models import Site
site = Site.objects.get_or_create(id=1)[0]
site.domain = 'mtrh-helpdesk.onrender.com'
site.name = 'MTRH IT Help Desk'
site.save()
print('Site domain set to mtrh-helpdesk.onrender.com')

from accounts.models import User
if not User.objects.filter(username='Admin').exists():
    u = User.objects.create_superuser(
        username='Admin',
        email='jebetmichelle7@gmail.com',
        password='Michelle@2026',
        first_name='Michelle',
        last_name='Kibichii',
    )
    u.role = 'admin'
    u.save()
    print('Admin user created')
else:
    u = User.objects.get(username='Admin')
    u.role = 'admin'
    u.first_name = 'Michelle'
    u.last_name = 'Kibichii'
    u.save()
    print('Admin updated')
EOF