# Drone Strike

Django project displaying all reported USA drone strikes.

## Quickstart

Clone the repo from GitHub:

    git clone https://github.com/sasakalaba/drone-strike.git

Create python3 virtualenv:

    apt-get install python3 python3-doc
    mkvirtualenv --python=/usr/bin/python3 drone-strike

Setup postgres:

    apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
    su - postgres
    psql

    postgres=# CREATE USER <username> WITH PASSWORD '<password>';
    postgres=# CREATE DATABASE drone-strike WITH OWNER <username>;

Navigate to project dir and install requirements:

    cd drone-strike
    pip install -r requirements.txt

Create .env file:

    cat .env_sample >> .env

Generate autokey:

    python -c "import string,random; uni=string.ascii_letters+string.digits+string.punctuation; print(repr(''.join([random.SystemRandom().choice(uni) for i in range(random.randint(45,50))])))"

Set .env values:

    nano .env

Run the migrations:

    python manage.py migrate

Create super user:

    python manage.py createsuperuser


## Automated tests

To run the automated test suite:

    python manage.py test --settings=project.settings.test


## Start server

Start the server:

    python manage.py collectstatic
    python manage.py runserver


## Management commands:
    python manage.py import_data
