#!/bin/bash

pkill -f gunicorn
sleep 1
d acumen
sleep 1
gunicorn app:app -b localhost:8000 &
sleep 1
sudo service nginx restart
echo 'Server up and running :)'

