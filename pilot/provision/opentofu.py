# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import json
import os
import subprocess
from typing import TYPE_CHECKING

import frappe
from cdktf import App, LocalBackend, TerraformStack
from constructs import Construct

from pilot.provision.doctype.provision_declaration.provision_declaration import ProvisionDeclaration
from pilot.provision.doctype.provision_plan.provision_plan import ProvisionPlan
from pilot.provision.doctype.provision_state.provision_state import ProvisionState
from pilot.provision.providers.digitalocean import DigitalOcean

if TYPE_CHECKING:
	from pilot.provision.doctype.region.region import Region


STACKS_DIRECTORY = "stacks"
OPENTOFU_BINARY = "tofu"


class PilotStack(TerraformStack):
	def __init__(self, scope: Construct, name: str, region: "Region"):
		super().__init__(scope, name)

		# Backend file by default is placed at
		# Which happens to be `sites/terraform.<region>.tfstate`
		# This moves it to the stack directory
		directory = os.path.abspath(frappe.get_site_path(STACKS_DIRECTORY))
		stack_directory = os.path.join(directory, "stacks", region.name)
		backend_file = os.path.join(stack_directory, "terraform.tfstate")
		LocalBackend(self, path=backend_file)

		DigitalOcean().provision(self, scope, name, region)


class OpenTofu:
	def __init__(self, region: "Region") -> None:
		self.region = region
		self.directory = os.path.abspath(frappe.get_site_path(STACKS_DIRECTORY))
		self.stack_directory = os.path.join(self.directory, "stacks", self.region.name)
		self.tofu = TofuCLI(self.stack_directory, region)

	def provision(self) -> None:
		self.synth()
		self.sync()
		self.init()
		self.plan()
		self.deploy()
		self.sync()

	def destroy(self) -> None:
		self.sync()
		self._destroy()
		self.sync()

	def synth(self) -> ProvisionDeclaration:
		# Creates sites/<site>/stacks directory on first run
		app = App(outdir=self.directory)
		PilotStack(app, self.region.name, self.region)
		app.synth()
		synth_file = os.path.join(self.directory, "stacks", self.region.name, "cdk.tf.json")
		with open(synth_file) as f:
			declaration = f.read()
			return self.create_declaration(declaration)

	def sync(self) -> ProvisionState:
		# We might not have any state to show in the beginning
		state, pretty_state = "{}", ""
		try:
			state = self.tofu.show()
			pretty_state = self.tofu.pretty_show()
		except Exception:
			pass
		return self.create_state(state, pretty_state)

	def init(self) -> str:
		# Creates the .terraform directory
		return self.tofu.init()

	def plan(self) -> ProvisionPlan:
		self.tofu.plan("tf.plan")
		plan = self.tofu.show("tf.plan")
		pretty_plan = self.tofu.pretty_show("tf.plan")
		return self.create_plan(plan, pretty_plan)

	def deploy(self) -> str:
		return self.tofu.apply("tf.plan")

	def _destroy(self) -> str:
		return self.tofu.destroy()

	def create_declaration(self, declaration: str) -> ProvisionDeclaration:
		return frappe.new_doc(
			"Provision Declaration", region=self.region.name, stack=self.region.name, declaration=declaration
		).insert()

	def create_plan(self, plan: str, pretty_plan: str) -> ProvisionPlan:
		return frappe.new_doc(
			"Provision Plan",
			region=self.region.name,
			stack=self.region.name,
			plan=json.dumps(json.loads(plan), indent=2),
			pretty_plan=pretty_plan,
		).insert()

	def create_state(self, state: str, pretty_state: str) -> ProvisionState:
		return frappe.new_doc(
			"Provision State",
			region=self.region.name,
			stack=self.region.name,
			state=json.dumps(json.loads(state), indent=2),
			pretty_state=pretty_state,
		).insert()


class TofuCLI:
	def __init__(self, path, region) -> None:
		self.path = path
		self.region = region

	def run(self, command) -> str:
		command = [OPENTOFU_BINARY, *command]
		process = subprocess.run(command, cwd=self.path, capture_output=True)
		output = process.stdout.decode()
		error = process.stderr.decode()

		parsed_output = self.parse_output(output)
		frappe.new_doc(
			"Provision Action",
			region=self.region.name,
			stack=self.region.name,
			action=command[1],
			output=output,
			error=error,
			parsed_output=parsed_output,
		).insert()
		return output

	def init(self) -> str:
		return self.run(["init", "-json"])

	def plan(self, file) -> str:
		return self.run(["plan", "-json", "-out", file])

	def apply(self, file) -> str:
		return self.run(["apply", "-json", file])

	def show(self, file: str | None = None) -> str:
		if file is None:
			return self.run(["show", "-json"])
		else:
			return self.run(["show", "-json", file])

	def pretty_show(self, file: str | None = None) -> str:
		if file is None:
			return self.run(["show", "-no-color"])
		else:
			return self.run(["show", file, "-no-color"])

	def destroy(self) -> str:
		return self.run(["destroy", "-json", "-auto-approve"])

	def parse_output(self, output: str) -> str:
		# Parse the output of the tofu command
		# Return the @message field on all lines
		parsed_lines = []
		for line in output.split("\n"):
			if not line:
				continue
			try:
				parsed_lines.append(json.loads(line)["@message"])
			except Exception:
				pass
		return "\n".join(parsed_lines)
