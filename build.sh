# Install dependencies
python -m pip install -r requirements.txt

# Create staticfiles directory
mkdir -p staticfiles_build/static

# Collect static files
python manage.py collectstatic --noinput

# Make migrations and apply them
python manage.py makemigrations
python manage.py migrate
