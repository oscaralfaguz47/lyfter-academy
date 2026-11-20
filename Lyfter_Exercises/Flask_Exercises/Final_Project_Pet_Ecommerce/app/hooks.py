""" Code that runs before and after every request. """

import logging
import re
import time
import uuid

from flask import Flask, Response, g, request

# a module logger. Its name is the module path, app.hooks, which is what we saw in the log line. 
logger = logging.getLogger(__name__)

# X-Request_ID is the conventional header name. Load balancers and API gateways use the same one.
REQUEST_ID_HEADER = "X-Request-ID"

# VALID_REQUEST_ID: a regex that allows only letters, digits, ., _ and -, up to 64 characters.
VALID_REQUEST_ID = re.compile(r"[A-Za-z0-9._-]{1,64}")


def register_hooks(app: Flask) -> None:
    app.before_request(_start_request)
    app.after_request(_finish_request)

# Runs before the route: if a proxy already sent and ID, we reuse it, so the sam ID follows the request across several services.
def _start_request() -> None:
    incoming_id = request.headers.get(REQUEST_ID_HEADER, "")
    # Good practice to validate: the ID gets written into logs. Without the check, a client could send a 10KB value or text that imitates a fake log line. Attack's name "log injection"
    g.request_id = incoming_id if VALID_REQUEST_ID.fullmatch(incoming_id) else uuid.uuid4().hex
    # time.perf_counter() is a high precision clock for measuring durations.
    g.start_time = time.perf_counter()

# Runs after the route and also after error responses: 
# it must receive and return the response. If we forget the return, every request crashes.
def _finish_request(response: Response) -> Response:
    # It adds the request id to the response
    response.headers[REQUEST_ID_HEADER] = g.get("request_id", "-")
    # It is a security header that tells browsers "trust my Content-Type, dont guess it"
    response.headers["X-Content-Type-Options"] = "nosniff"

    duration_ms = (time.perf_counter() - g.get("start_time", time.perf_counter())) * 1000
    # It passes the values as arguments, not inside an f-string.
    logger.info("%s %s -> %s (%.1f ms)", request.method, request.path, response.status_code, duration_ms)
    return response