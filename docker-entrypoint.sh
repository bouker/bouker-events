#!/usr/bin/env sh
CMD=$1

case "$CMD" in
  "init" )
    echo "Starting Bouker-Events service"
    sleep 10
    flask db upgrade
    /usr/local/bin/gunicorn --config server.ini app.wsgi:app
    ;;

esac

exec "$@"
