import os
from pygelf import GelfHttpHandler


class GraylogHandler(GelfHttpHandler):

    def emit(self, record):
        try:
            super(GraylogHandler, self).emit(record)
        except Exception as e:
            print("Cannot access remote Graylog Service: %s" % e)


host = os.environ.get('BOUKER_LOGGING_URL', '')
default_handler = GraylogHandler(host=host, port=12201, _facility='bouker-events')
