FROM python:3.6

RUN mkdir /bouker
WORKDIR /bouker
ADD . /bouker/
RUN pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "server.ini", "app.wsgi:app"]