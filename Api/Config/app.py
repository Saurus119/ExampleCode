from flask import Flask, send_file

from Api.Config.urls import register_api_routes
from Shared.RequestHooks.before_request_check import before_request_handler

app = Flask(__name__)

api_app = register_api_routes(app)
api_app.before_request(before_request_handler)

