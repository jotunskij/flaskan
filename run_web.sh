#!/bin/sh

TOKEN_SERVER=http://localhost:5001 \
SECRET_KEY=YOUR_APP_SECRET \
RECAPTCHA_SECRET=YOUR_RECAPTCHA_SECRET \
FLASK_APP=web.py poetry run python -m flask run