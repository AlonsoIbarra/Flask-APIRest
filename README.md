[![pipeline status](http://git.microbit.com/saul/ercomapi/badges/develop/pipeline.svg)](http://git.microbit.com/saul/ercomapi/commits/develop)

[![coverage report](http://git.microbit.com/saul/ercomapi/badges/develop/coverage.svg)](http://git.microbit.com/saul/ercomapi/commits/develop)

# ErcomAPI

APIRest to manage user auth for Ercom customers and products data.

# Run Docker Containers
To run api containers install [Docker compose](https://docs.docker.com/compose/install/) and exec the next commands:

$ cd docker

$ docker build -t ercom-api . -f Dockerfile

$ docker-compose up
