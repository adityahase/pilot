from flask import Flask, jsonify
from flask.views import MethodView

from .container import Container

application = Flask(__name__)


class ContainerAPI(MethodView):
	init_every_request = False

	def get(self):
		return jsonify(Container.list())

	def post(self):
		return jsonify(Container.create())


application.add_url_rule("/containers/", view_func=ContainerAPI.as_view("containers"))
