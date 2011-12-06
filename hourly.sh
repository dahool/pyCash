#!/bin/bash
cd /home/gabriel/public_html/pyCash
python manage.py updateevent
python manage.py syncexpenses
