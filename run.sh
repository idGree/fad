#!/bin/sh
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_RUN_PORT=8006
flask run
