from flask import send_file
from flask.views import MethodView

class DocumentationAPI(MethodView):

    def get(self):
        return send_file("../Config/openapi.json")