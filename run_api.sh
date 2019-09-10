#!/bin/sh

SECRET_KEY=YOUR_APP_SECRET \
RECAPTCHA_SECRET=YOUR_RECAPTCHA_SECRET \
FLASK_APP=api.py poetry run python -m flask run --port 5001