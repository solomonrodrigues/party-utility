# Install dependencies
python3.9 -m pip install -r requirements.txt

# Create staticfiles directory
mkdir -p staticfiles_build/static

# Collect static files
python3.9 manage.py collectstatic --noinput

# Make migrations and apply them
python3.9 manage.py makemigrations
python3.9 manage.py migrate
