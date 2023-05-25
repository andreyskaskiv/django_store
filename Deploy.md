
1. [x] [Initial Server Setup with Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-22-04)
2. [x] [How To Set Up Django with Postgres, Nginx, and Gunicorn on Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04)

---
# **AWS**

---
### 1. Connect to AWS 

```text
chmod 400 StoreCredentials.pem
ssh -i "StoreCredentials.pem" ubuntu@ec2-52-28-221-249.eu-central-1.compute.amazonaws.com
```

After project settings:
```text
cd store-server/store/

source ../venv/bin/activate

python manage.py shell_plus
```

---
### 2. Update & Upgrade

```text
sudo su

sudo apt update && apt upgrade -y
```
```text
sudo apt install mc
```

---
### 3. New Sudo Enabled User

* [How To Create A New Sudo Enabled User on Ubuntu 22.04 [Quickstart]](https://www.digitalocean.com/community/tutorials/how-to-create-a-new-sudo-enabled-user-on-ubuntu-22-04-quickstart)

_ubuntu@ip-172-31-26-130_  ---->  www-data
```text
usermod -a -G ubuntu www-data
```

---
### 4. Creating the PostgreSQL Database and User

```text
sudo apt install postgresql postgresql-contrib
```
```text
sudo -u postgres psql

\l
```

```text
- CREATE DATABASE shop_db_production;
- CREATE ROLE shop_username_production with password 'shop_password_production';
- ALTER ROLE "shop_username_production" WITH LOGIN;
- GRANT ALL PRIVILEGES ON DATABASE "shop_db_production" to shop_username_production;
- ALTER USER shop_username_production CREATEDB;
- GRANT postgres TO shop_username_production;
```

---
### 5. Creating a Python Virtual Environment for your Project

```text
mkdir store-server

cd store-server
```
```text
sudo apt install python3-venv
```
```text
python3 -m venv venv
```
```text
source venv/bin/activate
```

---
### 6. FileZilla

```text
Transferring a project
```

---
### 7. Refactoring file `.env`
```text
cd store/

nano .env

DATABASE_NAME=shop_db_production
DATABASE_USER=shop_username_production
DATABASE_PASSWORD=shop_password_production
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

```text
cd store-server/store/

source ../venv/bin/activate

python3 manage.py shell_plus

from django.conf import settings
settings.DATABASES
```

---
### 8. Installing packages from requirements.txt

```text
cd store-server/store

source ../venv/bin/activate
```

Check requirements.txt encoding in UTF-8 !!!
```text
pip install -r requirements.txt
```

```text
python manage.py migrate
python manage.py createsuperuser
```

---
### 9. STATIC

* [How to deploy static files](https://docs.djangoproject.com/en/4.2/howto/static-files/deployment/)

```text
cd store-server/store
source ../venv/bin/activate

python manage.py collectstatic
```

```text
python manage.py runserver 0.0.0.0:8000
```

http://52.28.221.249:8000


---
### 10. Gunicorn

* [Testing Gunicorn’s Ability to Serve the Project](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04#adjusting-the-project-settings)


```text
cd store-server/store
source ../venv/bin/activate

pip install gunicorn
```

```text
sudo nano /etc/systemd/system/gunicorn.socket
```
```text
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

```text
sudo nano /etc/systemd/system/gunicorn.service
```
```text
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/store-server/store
ExecStart=/home/ubuntu/store-server/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          store.wsgi:application

[Install]
WantedBy=multi-user.target
```
```text
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```
```text
sudo systemctl status gunicorn.socket
```
```text
sudo systemctl status gunicorn
```

Testing Socket Activation
```text
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

---
### 11. Nginx 

* [Configure Nginx to Proxy Pass to Gunicorn](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04#configure-nginx-to-proxy-pass-to-gunicorn)

```text
cd store-server/store
source ../venv/bin/activate

sudo apt install nginx
```
```text
sudo nano /etc/nginx/sites-available/store
```
```text
server {
    listen 80;
    server_name 52.28.221.249;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/store-server/store;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
```text
sudo ln -s /etc/nginx/sites-available/store /etc/nginx/sites-enabled
```
```text
sudo nginx -t
```
```text
sudo systemctl restart nginx
```

http://52.28.221.249


---
### 12. Redis 

* [How To Install and Secure Redis on Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-22-04)

```text
sudo apt install redis-server
```
```text
sudo nano /etc/redis/redis.conf
```
```text
. . .

# If you run Redis from upstart or systemd, Redis can interact with your
# supervision tree. Options:
#   supervised no      - no supervision interaction
#   supervised upstart - signal upstart by putting Redis into SIGSTOP mode
#   supervised systemd - signal systemd by writing READY=1 to $NOTIFY_SOCKET
#   supervised auto    - detect upstart or systemd method based on
#                        UPSTART_JOB or NOTIFY_SOCKET environment variables
# Note: these supervision methods only signal "process is ready."
#       They do not enable continuous liveness pings back to your supervisor.
supervised systemd

. . .
```
```text
sudo systemctl restart redis.service
```
```text
sudo systemctl status redis
```


---
### 13. Celery 

* [Celery, Usage systemd](https://docs.celeryq.dev/en/stable/userguide/daemonizing.html#usage-systemd)

```text
sudo nano /etc/systemd/system/celery.service
```
```text
[Unit]
Description=Celery Service
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/store-server/store

ExecStart=/home/ubuntu/store-server/venv/bin/celery -A store worker -l INFO

[Install]
WantedBy=multi-user.target
```
```text
sudo systemctl enable celery
```
```text
sudo systemctl start celery
```
```text
sudo systemctl status celery
```

---
### 14. Firewall 

* [Step 4 — Setting Up a Firewall](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-22-04#step-4-setting-up-a-firewall)

```text
sudo apt install ufw
```
```text
sudo ufw app list
```
```text
sudo ufw allow OpenSSH
```
```text
sudo ufw allow 'Nginx Full'
```
```text
sudo ufw enable
```
```text
sudo ufw status
```











