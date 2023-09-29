from flask import Flask

from ..Routes.countries_api import CountryAPI
from ..Routes.documentation_api import DocumentationAPI

def register_api_routes(app: Flask) -> Flask:
    """Register all routes that can be called as API endpoints."""
    app.add_url_rule("/openapi.json",  view_func= DocumentationAPI.as_view('documentation'), methods=["GET"])
    app.add_url_rule('/match_country', view_func= CountryAPI.as_view('country'), methods=["POST"])
    
    return app
