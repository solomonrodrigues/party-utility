# Party Utility 🎉

A lightweight web app for running party games in real life. One person opens a room, everyone joins with a 4-letter code, and the app handles the admin: who's playing, who's on which team, and what game to play next.

**Live:** [party-utility.vercel.app](https://party-utility.vercel.app)

## Features

- **Party rooms with join codes.** Create a room and share its 4-letter code (like `MTHL`). Friends join from their own phones, no account needed.
- **Live player list.** The room refreshes every few seconds, so new arrivals show up on every screen. The host can add or remove players by hand for anyone without a phone.
- **Random teams.** Pick how many teams (2–10) and players are shuffled and split evenly, each team with its own colour.
- **Random game picker.** Draws a game from the game library (managed in the Django admin), falling back to classics like Charades and Two Truths and a Lie. Each pick is logged as a game session for the party.

## Built with

- **Django 5.2** on Python 3.13
- **HTMX** for the interactive bits (forms, live player list, team generation) with no front-end build step
- **Tailwind CSS**
- **PostgreSQL**
- **Vercel** for hosting, using its Django preset

## How it works

The app is a single Django app, `partyutility`, with the data model in `partyutility/models.py`:

| Model | Purpose |
|---|---|
| `Party` | A room with a unique 4-letter code |
| `Player` | Someone in a party; the creator is marked as host |
| `Team` | A coloured team within a party, regenerated on each shuffle |
| `Game` | A game in the library: player counts, duration, materials, instructions |
| `GameSession` | A record of a game picked during a party |

Every page action is a small HTMX request that returns an HTML partial (`partyutility/templates/partyutility/partials/`), so the views stay as plain Django views and there's no JavaScript to maintain.

## Running locally

You'll need Python 3.13 and Docker (for Postgres).

```bash
# Start a Postgres database
docker run -d --name partydb -p 5432:5432 \
  -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=partydb postgres:16

# Install dependencies and set up the database
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
POSTGRES_HOST=localhost python manage.py migrate

# Run the dev server
POSTGRES_HOST=localhost python manage.py runserver
```

Then open http://localhost:8000. To add games to the library, create an admin user with `python manage.py createsuperuser` and visit `/admin/`.

Settings live in `api/settings/`: `development.py` is used locally, `production.py` on Vercel.

## Deployment

Pushes to `main` deploy to Vercel. The build runs `vercel_build.py`, which applies migrations on production deploys, and Vercel collects static files automatically. Production needs these environment variables:

- `DJANGO_SETTINGS_MODULE=api.settings.production`
- `SECRET_KEY`
- `POSTGRES_HOST`, `POSTGRES_DATABASE`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
