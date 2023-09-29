from flask import Flask

from FrontEnd.views import CountryView

def register_frontend_views(app: Flask) -> Flask:
    """All views that belongs under frontend."""
    app.add_url_rule('/', view_func= CountryView.as_view('all_countries'), methods=["GET", "DELETE", "POST"])
    
    return app
