from flask import request
from functools import wraps

def restrict_by_auth_token(allowed_methods):
    """Use this decorator to set which endpoints for API need Authorization token in the request headers."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.method in allowed_methods:
                auth_token = request.headers.get("Authorization")
                if not auth_token:
                    # here it can be extended to modify how the request behave. For demo it just has print.
                    print("Authentication token is missing. For now bypassing this check.")
            return func(*args, **kwargs)
        return wrapper
    return decorator