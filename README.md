[![pipeline status](http://git.microbit.com/saul/ercomapi/badges/develop/pipeline.svg)](http://git.microbit.com/saul/ercomapi/commits/develop)

[![coverage report](http://git.microbit.com/saul/ercomapi/badges/develop/coverage.svg)](http://git.microbit.com/saul/ercomapi/commits/develop)

# ErcomAPI

APIRest to manage user auth for Ercom customers and products data.
This API was develop using:
- [Flask](https://flask.palletsprojects.com/en/2.2.x/).
- [FlaskRESTfull](https://flask-restful.readthedocs.io/en/latest/).
- [flask-restful-swagger](https://flask-restful-swagger.readthedocs.io/en/latest/).
- [flask_sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/).

# Run Docker Containers
To run api containers install [Docker compose](https://docs.docker.com/compose/install/) and exec the next commands:

$ cd docker

$ docker build -t ercom-api . -f Dockerfile

$ docker-compose up


# Swagger documentation

To see endpoints and data required startup docker containers and got to http://{host}/api/spec.html

# Flask command line

If you want to handle models directly you can use flask shell by the next commands.

- Start docker containers.
- List docker containers by run 'Docker ps'
- Go to ercom-api container by run 'Docker exec -ti {ERCOM_CONTAINER_ID} bash'
- Run 'flask shell'
- Run 'from config import Client, Product, Category'
- Now you can work with model ORM's

For more information about Flask SQLAlchemy go to https://flask.palletsprojects.com/en/2.2.x/patterns/sqlalchemy/#manual-object-relational-mapping 
