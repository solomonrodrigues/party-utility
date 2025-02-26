echo "BUILD START"
python3 -m pip install --upgrade pip || { echo "pip upgrade failed"; exit 1; }
python3 -m pip install -r requirements.txt || { echo "requirements install failed"; exit 1; }
mkdir -p staticfiles_build/static
python3 manage.py collectstatic --noinput --clear --settings=api.settings.production || { echo "collectstatic failed"; exit 1; }

# Make migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Get the superuser username from the environment variable
superuser_username="$DJANGO_SUPERUSER_USERNAME"

# Check if superuser with the specified username already exists
if python3 manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(username='$superuser_username').exists())" 2>/dev/null | grep -q "False"; then
    python3 manage.py createsuperuser --noinput --username="$superuser_username"
    echo "Superuser created"
else
    echo "Superuser with specified username already exists"
fi

echo "BUILD END"