from flask import request, jsonify

def before_request_handler():
    """Check if the request includes the proper Content-Type in the header for request types that can manipulate data."""

    if request.method != "GET" and request.headers['Content-Type'] != 'application/json':
        return jsonify(), 415