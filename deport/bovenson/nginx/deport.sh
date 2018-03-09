#!/bin/bash
sudo rm /etc/nginx/sites-enabled/mixoj_nginx.conf
sudo ln -s /home/ubuntu/venv/mixoj/deport/bovenson/nginx/mixoj_nginx.conf /etc/nginx/sites-enabled/mixoj_nginx.conf
sudo service nginx restart
