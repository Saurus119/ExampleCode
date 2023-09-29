from flask import Flask

from FrontEnd.Config.urls import register_frontend_views

# create instance of the frontend app and all related config to it.
frontend_app = Flask(__name__, template_folder="../templates/", static_folder="../static/")
frontend_app = register_frontend_views(frontend_app)
