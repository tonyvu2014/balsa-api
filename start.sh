#!/bin/bash

source venv/bin/activate
pip install -r requirements.txt
cd balsa && gunicorn -b 0.0.0.0:8000 -k gevent -p /var/run/gunicorn.pid --error-logfile /var/log/balsa/error.log -D balsa.wsgi 
