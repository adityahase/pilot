import requests


class Agent:
	def __init__(self, node):
		self.node = node

	def create_machine(self, machine):
		response = requests.post(f"http://{self.node}/machines", json=machine)
		return response.status_code == 201

	def stop_machine(self, machine):
		response = requests.post(f"http://{self.node}/machines/{machine}/actions/stop")
		return response.status_code == 204

	def terminate_machine(self, machine):
		response = requests.delete(f"http://{self.node}/machines/{machine}")
		return response.status_code == 204
