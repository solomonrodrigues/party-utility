# Install dependencies
pip install -r requirements.txt

mkdir -p staticfiles_build/static

python3.9 manage.py collectstatic

# Make migrations
python3.9 manage.py makemigrations
python3.9 manage.py migrate