import requests


class Agent:
	def __init__(self, node):
		self.node = node

	def create_machine(self, machine):
		response = requests.post(f"http://{self.node}/machines", json=machine)
		return response.status_code == 201
