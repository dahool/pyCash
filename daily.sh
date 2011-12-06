#!/bin/bash
cd /home/gabriel/public_html/pyCash
python manage.py autodebits
python dbbackup.py
