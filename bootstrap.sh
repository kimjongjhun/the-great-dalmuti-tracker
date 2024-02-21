#!/bin/sh
export FLASK_APP=./hello.py
pipenv run flask --debug run -h 0.0.0.0