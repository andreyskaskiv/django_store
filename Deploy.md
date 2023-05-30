
1. [x] [Initial Server Setup with Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-22-04)
2. [x] [How To Set Up Django with Postgres, Nginx, and Gunicorn on Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04)

---
# **AWS**
 
1. <a href="#connect_to_aws">Connect to AWS</a>
2. <a href="#update_upgrade">Update & Upgrade</a>
3. <a href="#new_sudo_enabled_user">New Sudo Enabled User</a>
4. <a href="#creating_the_postgre_sql_database_and_user">Creating the PostgreSQL Database and User</a>
5. <a href="#creating_a_python_virtual_environment_for_your_project">Creating a Python Virtual Environment for your Project</a>
6. <a href="#file_zilla">FileZilla</a>
7. <a href="#refactoring_file_env">Refactoring file `.env`</a>
8. <a href="#requirements">Installing packages from requirements.txt</a>
9. <a href="#static">STATIC</a>
10. <a href="#gunicorn">Gunicorn</a>
11. <a href="#nginx">Nginx</a>
12. <a href="#redis">Redis</a>
13. <a href="#celery">Celery</a>
14. <a href="#firewall">Firewall</a>
15. <a href="#domain_name">Domain name</a>
16. <a href="#certbot">SSL certificates, Certbot</a>
17. <a href="#fixtures_media">Fixtures, Media</a>
18. <a href="#email">Email</a>
19. <a href="#oauth_git_hub">OAuth GitHub</a>
20. <a href="#stripe">Stripe</a>



---
### 1. Connect to AWS: <a name="connect_to_aws"></a>

```text
chmod 400 StoreCredentials.pem
ssh -i "StoreCredentials.pem" ubuntu@ec2-52-28-221-249.eu-central-1.compute.amazonaws.com
```
---
test card for payment:  
`4242 4242 4242 4242`
---
**After project settings:**

shell_plus:
```text
cd store-server/store/

source ../venv/bin/activate

python manage.py shell_plus
```
nginx:
```text
sudo systemctl restart nginx
sudo nginx -t
sudo systemctl status nginx
```
```text
tail -f /var/log/nginx/access.log
```
gunicorn:
```text
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```
celery:
```text
sudo systemctl restart celery
sudo systemctl status celery
```
Server resolves:
```text
nslookup clothing-store.pp.ua
```
```text
nslookup clothing-store.pp.ua 8.8.4.4 
```
Open ports:
```text
nmap clothing-store.pp.ua
```
```text
telnet 52.28.221.249 80
telnet clothing-store.pp.ua 80
```
Сheck that the domain name resolves to the correct IP address:
```text
dig clothing-store.pp.ua
```

---
### 2. Update & Upgrade: <a name="update_upgrade"></a>

```text
sudo su

sudo apt update && apt upgrade -y
```
```text
sudo apt install mc
```

---
### 3. New Sudo Enabled User: <a name="new_sudo_enabled_user"></a>

* [How To Create A New Sudo Enabled User on Ubuntu 22.04 [Quickstart]](https://www.digitalocean.com/community/tutorials/how-to-create-a-new-sudo-enabled-user-on-ubuntu-22-04-quickstart)

_ubuntu@ip-172-31-26-130_  ---->  www-data
```text
usermod -a -G ubuntu www-data
```

---
### 4. Creating the PostgreSQL Database and User: <a name="creating_the_postgre_sql_database_and_user"></a>

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
### 5. Creating a Python Virtual Environment for your Project: <a name="creating_a_python_virtual_environment_for_your_project"></a>

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
### 6. FileZilla: <a name="file_zilla"></a>

```text
Transferring project files to the server
```

---
### 7. Refactoring file `.env` : <a name="refactoring_file_env"></a>
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
### 8. Installing packages from requirements.txt: <a name="requirements"></a>

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
### 9. STATIC: <a name="static"></a>

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
### 10. Gunicorn: <a name="gunicorn"></a>

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
### 11. Nginx: <a name="nginx"></a>

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
enable or disabled the file:
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

Info:
```text
tail -f /var/log/nginx/access.log
```
```text
tail -f /var/log/nginx/error.log
```
```text
tail -f /var/log/nginx/*.log
```
What servers do we have running:
```text
sudo ls -l /etc/nginx/sites-enabled
```





---
### 12. Redis: <a name="redis"></a>

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
### 13. Celery: <a name="celery"></a>

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
### 14. Firewall: <a name="firewall"></a>

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

---
### 15. Domain name: <a name="domain_name"></a>

* [Configure Nginx to Proxy Pass to Gunicorn](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04#configure-nginx-to-proxy-pass-to-gunicorn)

domain = clothing-store.pp.ua

```text
sudo nano /etc/nginx/sites-available/store
```
```text
server {
    listen 80;
    server_name clothing-store.pp.ua;

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
sudo systemctl restart nginx
sudo nginx -t
```
```text
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```
```text
sudo systemctl restart celery
sudo systemctl status celery
```

http://clothing-store.pp.ua


---
### 16. Certbot: <a name="certbot"></a>

* [Step 1 — Installing Certbot](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-22-04#step-1-installing-certbot)

```text
sudo snap install core; sudo snap refresh core
```
```text
sudo snap install --classic certbot
```
```text
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```
```text
sudo certbot --nginx -d clothing-store.pp.ua
```
```text
sudo nano /etc/nginx/sites-available/store
```

---
### 17. Fixtures, Media: <a name="fixtures_media"></a>

```text
ssh -i "StoreCredentials.pem" ubuntu@ec2-52-28-221-249.eu-central-1.compute.amazonaws.com
cd store-server/store/
source ../venv/bin/activate
```
```text
python manage.py loaddata products/fixtures/categories.json
python manage.py loaddata products/fixtures/goods.json
```
```text
FileZilla  ->  copy media
```
```text
sudo nano /etc/nginx/sites-available/store
```
```text
server {
    listen 80;
    server_name clothing-store.pp.ua;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/store-server/store;
    }
    
    location /media/ {
        root /home/ubuntu/store-server/store;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
```text
sudo systemctl restart nginx
sudo nginx -t
```
```text
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```
```text
sudo systemctl restart celery
sudo systemctl status celery
```

---
### 18. Email: <a name="email"></a>

```text
cd store-server/store/
```
```text
nano .env
```
```text
DOMAIN_NAME=https://clothing-store.pp.ua
```
```text
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```
```text
sudo systemctl restart celery
sudo systemctl status celery
```

---
### 19. OAuth GitHub: <a name="oauth_git_hub"></a>

* App registration (get your key and secret here):  
    [github.com](https://github.com/settings/applications/new) 

* Development callback URL:  
    http://52.28.221.249/accounts/github/login/callback/  
    or  
    https://clothing-store.pp.ua/accounts/github/login/callback/

* Shell_plus:

```text
cd store-server/store/

source ../venv/bin/activate

python manage.py shell_plus

>>> Site.objects.all()
<QuerySet [<Site: github.com>]>

>>> Site.objects.filter(domain="github.com").values('id')
<QuerySet [{'id': 1}]>
```

* Admin panel (Select site to change): 

[SITE_ID](http://52.28.221.249/admin/sites/site/) - put PK github  
[SITE_ID](https://clothing-store.pp.ua/admin/sites/site/) - put PK github

```text
cd store
```
```text
nano settings.py
```
```
SITE_ID = 1
```
  
* Admin panel (Select social application to change): 

[Add social application](https://clothing-store.pp.ua/admin/socialaccount/socialapp/add/)


---
### 20. Stripe: <a name="stripe"></a>  

* [Take webhooks live](https://stripe.com/docs/webhooks/go-live)
* [webhooks](https://dashboard.stripe.com/webhooks)

Listen to Stripe events
Endpoint URL:
```text
https://clothing-store.pp.ua/webhook/stripe/
```
Listen to:
```text
checkout.session.completed
```
Server
```text
cd store-server/store/
```
```text
nano .env
```
```text
STRIPE_WEBHOOK_SECRET=whsec_DPDxMqK7v9PDUAKEAwmu8XcCEGG8SmiN5i
```
```text
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```
```text
sudo systemctl restart celery
sudo systemctl status celery
```
Check `Stripe product price id`


test card for payment:  
`4242 4242 4242 4242`


