# Setup

## Requirements

- Database: SQLite, MySQL, PostgresQL or anything that is supported by 
  [SQLAlchemy][SQLAlchemy]
- Redis
- SMTP

## Application Configuration

Application configuration is required as on `.env.example`.
You can copy this file as `.env` and edit it as you want.

```shell
cp .env.example .env
```

## Database

### Create Tables

```bash
# Initial alembic
alembic revision --autogenerate -m 'initial'
alembic upgrade head
```

## Redis

Redis is required for [`arq`][arq] for 
job queues and RPC in python with asyncio and redis.

## SMTP

Upon **registration**, **password update**, **reset password** action,
you need to open links that sent to your email.

White starting this web application, 
you can use a really cool **fake SMTP** service that provided by 
[Ethereal Email][ethereal].

For production use, you may edit the SMTP configuration on the `.env` file
for any SMTP service you like.

## Admin User

On first startup, an `admin` user is created.
The credentials should be placed on `.env` file.

Admin configuration example on `.env` file

```text
ADMIN_USERNAME=admin
ADMIN_PASSWORD=password
ADMIN_EMAIL='admin@localhost'
```

# Run Locally (Development Mode)

## Web Application Service

```shell
bash scripts/dev.sh
```

## Arq (Job Queueing and Processing)

```shell
bash scripts/arq.sh
```

# Run In Production

For production use, make sure you edit the `.env` configuration file, such as.
Make sure you use proper value for `SECRET_KEY` and admin user credentials.

```text
ENV=prod
SECRET_KEY=CHANGE THIS SECRET

ADMIN_USERNAME=admin
ADMIN_PASSWORD=password
ADMIN_EMAIL='admin@localhost'
```

Then make sure you use a real SMTP Provided and edit the SMTP configuration.

## Web Application Service

```shell
bash scripts/prod.sh
```

## Arq (Job Queueing and Processing)

```shell
bash scripts/arq.sh
```

## KIll the services

```shell
kill `cat files/pids/web_app.pid`
```

## Nginx

Please take a look on `files/config/nginx_conf_d_yousite.conf`.
Copy that file and edit on `/etc/nginx/conf.d/yoursite_com.conf`.

## SSL Certificate

Please consider to create a free SSH Certificate you your web app. :)

[Letsencrypt][Letsencrypt] will help you to run your web application to this.

# Test

## Install Test Packages

```shell
pip install -r requirements/test.txt
```

## Run Test

```shell
pytest
```


[arq]: https://arq-docs.helpmanual.io
[ethereal]: https://ethereal.email
[Letsencrypt]: https://letsencrypt.org
[SQLAlchemy]: https://docs.sqlalchemy.org/en/20/
