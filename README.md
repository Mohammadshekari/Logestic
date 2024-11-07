<h1 align="center">Django APP_NAME  MicroService</h1>
<h3 align="center">Small Service to get APP_DESCRIPTION through api</h3>    

# Guideline
- [Guideline](#guideline)
- [Database Schema](#database-schema)
- [Development usage](#development-usage)
  - [Environment Variables](#environment-variables)
  - [Build everything](#build-everything)
- [Note](#note)
- [Check it out in a browser](#check-it-out-in-a-browser)
- [Testing](#testing)
  - [Running all tests](#running-all-tests)
- [Production usage](#production-usage)
- [Access Swagger API](#access-swagger-api)
- [Django Dump and Load Data](#django-dump-and-load-data)
- [License](#license)
- [Todo](#todo)
- [Bugs](#bugs)

# Database Schema
this is the schema which have been used to create this app. which includes the database design.

![Semantic description of image](/docs/database_schema.png "Current Diagram")

# Development usage
first of all clone this repository

```sh
git clone APP_REPOSITORY_URL
```

## Environment Variables

while using dev mode all the environment variables can be found inside envs folder for dev purposes which are included in docker-compose.yml file for debugging mode and you are free to change commands inside:

```docker
services:
  backend:
    ...
    env_file:
      - ./envs/dev/django/.env
    ...
```
also for other services there are .env files according to them.

Note: backend, worker and beater are all using the same env file.

## Build everything

*The first time you run this it's going to take 5-10 minutes depending on your
internet connection speed and computer's hardware specs. That's because it's
going to download a few Docker images and build the Python + requirements dependencies.*

note: before starting the build for stage please create the bridge network.
```sh
docker network create -d bridge shared
```

```sh
docker-compose up --build
```

Now that everything is built and running we can treat it like any other Django
app.

# Note

If you receive an error about a port being in use? Chances are it's because
something on your machine is already running on port 8000. then you have to change the docker-compose.yml file according to your needs.
# Check it out in a browser

Visit <http://localhost:8000/api/APP_NAME/swagger> in your favorite browser.

# Testing
## Running all tests
for testing purposes i have provided the dependencies for pytest and you can simply run the tests you have created with the command below:

```sh
docker compose exec backend sh -c sh -c "pytest." 
```

in order to test specific directory use the following command:
```bash
docker-compose exec backend sh -c "pytest ./API_URL/PATH/"
```


if you also wanted to test the pep8 and writing lints you can run the below command:

```sh
docker compose exec backend sh -c sh -c " black -l 79 && flake8" 
```
note: all the base configs can be found in pytest.ini and .flake8

# Production usage
will be provided ...


# Access Swagger API
if you needed to see the api docs on swagger you can use the following url in dev mode:
```
http://localhost:8000/api/APP_NAME/swagger
```

# Django Dump and Load Data
in order to dump data from current data base, you can use the following command:
```sh
docker-compose exec backend sh -c "python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > backup-db.json"
```
and also if you need to load the data all you have to do is to use this command:
```sh
docker-compose exec backend sh -c "python manage.py loaddata backup-db.json"

```
# License
APACHE.

# Todo


# Bugs
