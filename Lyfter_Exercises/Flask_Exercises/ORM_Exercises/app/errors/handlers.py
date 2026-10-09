""" Turn exceptions into RFC 9457 Problem Details JSON responses. """

from http import HTTPStatus

from flask import Flask, Response, jsonify, request
from werkzeug.exceptions import HTTPException

from app.errors.exceptions import ConflictError, DomainError, NotFoundError, ValidationError

PROBLEM_CONTENT_TYPE = "application/problem+json"

#------------------------------------------ HTTP STATUS GUIDE FOR THIS API --------------------------------------------------------
# 
# Success (returned by routes)
#   200 OK                      -> GET found it, PUT/PATCH updated it (with body)
#   201 Created                 -> POST resource created (add a location header)
#   204 No Content              -> DELETE succeeded (no body)
#
# Raised by us (domain errors -> mapped below)
#   404 Not Found               -> NotFoundError: the resource id does not exist
#   409 Conflict                -> ConflictError: conflicts with the current state (duplicate email, username, car already rented)
#   422 Unprocessable           -> ValidationError: JSON is valid but values are wrong
#
# Raised automatically by Flask/Werkzeug (no code needed)
#   400 Bad Request             -> body is not valid JSON
#   404 Not Found               -> The URL does not match any route
#   405 Method Not Allowed      -> The route exists but wrong method (calling POST to a GET method)
#   413 Content Too Large       -> body bigger than MAX_CONTENT_LENGTH
#   415 Unsupported Media       -> body sent without Content-Type: application/json
#   500 Internal Error          -> unhandled exception (a bug), logged, never detailed
#
# Added later, when we need them
#   401 Unauthorized            -> Not logged in / invalid token (authentication)
#   403 Forbidden               -> Logged in but not allowed (authorization)
#   429 Too Many Requests       -> Rate limit exceeded
#   503 Service Unavailable     -> A dependency is down 
#----------------------------------------------------------------------------------------------------------------------------------


# The unique place where a domain error it's translated to HTTP code
# STATUS_BY_ERROR is a type hint "dict[type[DomainError], HTTPStatus]"  
STATUS_BY_ERROR: dict[type[DomainError], HTTPStatus] = {
    NotFoundError: HTTPStatus.NOT_FOUND,                  # 404
    ConflictError: HTTPStatus.CONFLICT,                   # 409
    ValidationError: HTTPStatus.UNPROCESSABLE_ENTITY,     # 422
}

# This tells to Flask "When this class or subclass of exception is thrown, then call to this function"
def register_error_handlers(app: Flask) -> None:
    app.register_error_handler(DomainError, _handle_domain_error)
    # HTTPException is the Werkzeug class, the library upon which Flask is built, for HTTP errors, 404, 405, malformed JSON and body too big.
    app.register_error_handler(HTTPException, _handle_http_exception)

# This is the function that builds the response
def problem(status: HTTPStatus, detail: str | None = None, errors: dict | None = None) -> Response:
    """ Build a Problem Details response. """
    body = {
        "type": "about:blank",
        "title": status.phrase,   # It gives the standard name, ex: "Not Found"
        "status": status.value,   # 404
        "details": detail,
        "instance": request.path, # The route of the current request
    }
    if errors:
        body["errors"] = errors
    response = jsonify(body)  # Converts the dict in a JSON response
    response.status_code = status.value
    response.content_type = PROBLEM_CONTENT_TYPE
    return response

def _handle_domain_error(error: DomainError) -> Response:
    # type(error) gets the exact class, ex: NotFoundError
    # .get(..., BAD_REQUEST): if we create a new DomainError and forget to add it in the dict it falls as 400 instead of crashing 
    status = STATUS_BY_ERROR.get(type(error), HTTPStatus.BAD_REQUEST) 
    return problem(status, error.message, error.details)

def _handle_http_exception(error: HTTPException) -> Response:
    """ 404 unknown route, 405 wrong method, 400 bad JSON, 413 too large, 500 unexpected. """
    response = problem(HTTPStatus(error.code), error.description) # error.code is the number (404, 405...) and error.description is the Werkzeug message

    # Some errors brings required headers, for the client to know what methods they can use, we skip "Content-Type" because ours is "problem+json"
    for name, value in error.get_headers():
        if name.lower() != "content-type":
            response.headers[name] = value
    return response

# NOTES FOR UNDERSTANDING
# What about unexpected errors like bugs or 1/0?, Flask already registers the traceback in the log and converts it to a 500 
# that our HTTPException handler responds in Problem Details, the client never sees internal details
