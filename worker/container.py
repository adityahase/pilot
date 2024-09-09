import json
import shlex
from subprocess import check_output


class Container:
	@staticmethod
	def list():
		command = shlex.split("nerdctl container ls --no-trunc --format '{{json .}}'")
		return [json.loads(line) for line in check_output(command).splitlines()]

	@staticmethod
	def create():
		command = shlex.split("nerdctl container run --detach redis:alpine")
		return {"name": check_output(command).decode()}
