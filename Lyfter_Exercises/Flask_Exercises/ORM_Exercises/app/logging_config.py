""" Logging setup: one format for the whole app, with the request ID on every line. """

import logging

from flask import g, has_request_context

# asctime: is the timestamp. levelname: is INFO or ERROR, the -8 pads it to 8 chars so the columns line up
# request_id: our custom field. name: is the logger name, so we know which file wrote the line. message: is our text. 
LOG_FORMAT = "%(asctime)s %(levelname)-8s [%(request_id)s] %(name)s: %(message)s"


# Python calls this method for every log record before printing it, we attach "request_id" to the record.
class RequestIdFilter(logging.Filter):
    """ Add the current request ID to every log record. """

    def filter(self, record: logging.LogRecord) -> bool:
        # Here it checks if we are inside a request. At startup or in a CLI command there is no request, and touching g there would crash, so we user "-"
        record.request_id = g.get("request_id", "-") if has_request_context() else "-"
        return True 

def configure_logging(level:str) -> None:
    # StreamHandler writes to stderr. That's the best practice for servers and containers, the app writes to the stream and the platform (Docker, systemd, Azure)
    # collects it. The app shouldn't manage log files itself.
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    handler.addFilter(RequestIdFilter())

    # Logging.getLogger with no name returns the root logger, the parent of the loggers. Configuring it once covers every logger in the app, including SQLAlchemy's.
    root = logging.getLogger()
    # root.handlers = [handler] replaces the list instead of appending to it. Tests call create_app() many times, and appending would print every line 2,3,4 times.
    root.handlers = [handler] 
    root.setLevel(level)