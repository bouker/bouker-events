# bouker-events


![Build Status](https://travis-ci.org/bouker/bouker-events.svg?branch=master)

## Migrations

    flask db migrate
    flask db upgrade


## Docker

    docker build -t roxel/bouker-events .
    docker run -p 8000:8000 roxel/bouker-events