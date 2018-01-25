import os
from pygelf import GelfHttpHandler


host = os.environ.get('BOUKER_LOGGING_URL')
default_handler = GelfHttpHandler(host=host, port=12201, _facility='bouker-events')
