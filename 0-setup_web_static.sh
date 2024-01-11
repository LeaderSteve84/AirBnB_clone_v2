#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static.
echo -e "Updating Advance package tool and installing nginx........\n"

sudo apt-get update
sudo apt-get install nginx -y

echo -e "allowing uncomplicated firewall.....\n"

sudo ufw allow 'Nginx HTTP'

echo -e "Creating directory structure.....\n"

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

echo -e "Creating empty file......\n"

sudo touch /data/web_static/releases/test/index.html

echo -e "writing into the empty file.....\n"

sudo echo "<html>
                <head>
                </head>
                <body>
                        I love Holberton School
                </body>
           </html>" | sudo tee /data/web_static/releases/test/index.html

echo -e "Creating Symbolic link.....\n"

sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

echo -e "Giving ownership of the /data/ folder to the ubuntu user AND group.....\n"

sudo chown -R ubuntu:ubuntu /data/

echo -e "Updating the Nginx configuration.......\n"

sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

echo -e "Installation and configuration is successful. Restarting nginx......\n"
sudo service nginx restart
