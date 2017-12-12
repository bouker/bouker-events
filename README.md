# bouker-events


![Build Status](https://travis-ci.org/bouker/bouker-events.svg?branch=master)

## Migrations

    flask db migrate
    flask db upgrade


## Docker

Image is hosted on [Docker Hub](https://hub.docker.com/r/roxel/bouker-events/) but can be built locally using:

    docker build -t roxel/bouker-events .

To run the image locally use Compose (it will mount code as a volume - use code available on the host machine)

    docker-compose up

Or use `docker run`:

* link port 8000 in a container `-p 8000:8000`
* supply environment variable `SQLALCHEMY_DATABASE_URI` in format {engine}://{user}:{password}@{host}/{database}, e.g.:
    
    SQLALCHEMY_DATABASE_URI=postgresql://bouker_events:passwd123@db/bouker_events
