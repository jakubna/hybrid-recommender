#!/bin/bash
source venv/bin/activate

exec gunicorn -b :8020 --access-logfile - --error-logfile - main:app