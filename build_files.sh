echo "BUILD START"
python3 -m pip install --upgrade pip || { echo "pip upgrade failed"; exit 1; }
python3 -m pip install -r requirements.txt || { echo "requirements install failed"; exit 1; }
python3 manage.py collectstatic --noinput --clear --settings=api.settings.production || { echo "collectstatic failed"; exit 1; }
echo "BUILD END"