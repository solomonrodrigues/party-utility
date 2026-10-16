"""Vercel build step: apply migrations on production deploys only. Vercel runs collectstatic itself."""
import os

import django
from django.core.management import call_command

# Previews have no POSTGRES_* env vars, so migrating there would fail the build.
if os.environ.get("VERCEL_ENV") == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings.production")
    django.setup()
    call_command("migrate", interactive=False)
else:
    print(f"Skipping migrate on VERCEL_ENV={os.environ.get('VERCEL_ENV')}")
