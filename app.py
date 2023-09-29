from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from Api.Config.app import api_app
from FrontEnd.Config.app import frontend_app

def create_app():
    application = Flask(__name__)
    application.wsgi_app = DispatcherMiddleware(
        frontend_app, {
            '/api': api_app
        })
    return application

if __name__ == "__main__":
    application = create_app()
    application.run(host='0.0.0.0', debug=True)