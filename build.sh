#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput 