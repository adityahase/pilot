import json
import subprocess

import ansible_runner
import frappe
import wrapt
from frappe.utils import now_datetime as now


def reconnect_on_failure():
	@wrapt.decorator
	def wrapper(wrapped, instance, args, kwargs):
		try:
			return wrapped(*args, **kwargs)
		except Exception as e:
			if frappe.db.is_interface_error(e):
				frappe.db.connect()
				return wrapped(*args, **kwargs)
			raise

	return wrapper


class Ansible:
	def __init__(self, node, playbook, user="root", variables=None, port=22):
		self.node = node
		self.playbook = playbook
		self.playbook_path = frappe.get_app_path("pilot", "infrastructure", "playbooks", self.playbook)
		self.host = node.public_ip_address
		self.variables = variables or {}
		self.user = user
		self.create_ansible_play()

	def create_ansible_play(self):
		# Parse the playbook and create Ansible Tasks so we can show how many tasks are pending
		# Assume we only have one play per playbook
		play = self._get_play()
		play_doc = frappe.get_doc(
			{
				"doctype": "Ansible Play",
				"node": self.node.name,
				"variables": json.dumps(self.variables, indent=4),
				"playbook": self.playbook,
				"play": play["name"],
			}
		).insert()
		self.play = play_doc.name
		self.tasks = {}
		self.task_list = []
		for task in play["tasks"]:
			task_doc = frappe.get_doc(
				{
					"doctype": "Ansible Task",
					"play": self.play,
					"role": task["role"],
					"task": task["task"],
				}
			).insert()
			self.tasks.setdefault(task["role"], {})[task["task"]] = task_doc.name
			self.task_list.append(task_doc.name)

	def run(self):
		# Note: ansible-runner sets awx_display as the DisplayCallBack
		# awx_display listens to the ansible output and emits events for easier consumption

		ansible_runner.run(
			playbook=self.playbook_path,
			inventory=self.host,
			extravars=self.variables,
			cmdline=f"--user={self.user}",
			event_handler=self.event_handler,
		)
		return frappe.get_doc("Ansible Play", self.play)

	def event_handler(self, event):
		event_type = event.get("event")
		if hasattr(self, event_type):
			method = getattr(self, event_type)
			if callable(method):
				method(event.get("event_data"))

	def playbook_on_start(self, event):
		self.update_play("Running")

	def playbook_on_stats(self, event):
		stats = {}
		for key in ["changed", "dark", "failures", "ignored", "ok", "processed", "rescued", "skipped"]:
			stats[key] = event.get(key, {}).get(self.host, 0)
		stats["unreachable"] = stats.pop("dark", 0)  # ansible_runner quirk
		self.update_play(stats=stats)

	def playbook_on_task_start(self, event):
		self.update_task("Running", task=event)

	def runner_on_ok(self, event):
		self.update_task("Success", event)
		self.process_task_success(event)

	def runner_on_failed(self, event):
		self.update_task("Failure", result=event)

	def runner_on_skipped(self, event):
		self.update_task("Skipped", result=event)

	def runner_on_unreachable(self, event):
		self.update_task("Unreachable", result=event)

	@reconnect_on_failure()
	def process_task_success(self, event):
		result, action = frappe._dict(event.get("res", {})), event.get("task_action")
		if action == "user":
			node_name = frappe.db.get_value("Ansible Play", self.play, "node")
			node = frappe.get_doc("Node", node_name)
			if result.name == "root":
				node.root_public_key = result.ssh_public_key
			if result.name == "frappe":
				node.frappe_public_key = result.ssh_public_key
			node.save()

	@reconnect_on_failure()
	def update_play(self, status=None, stats=None):
		play = frappe.get_doc("Ansible Play", self.play)
		if stats:
			play.update(stats)
			if play.failures or play.unreachable:
				play.status = "Failure"
			else:
				play.status = "Success"
			play.end = now()
			play.duration = (play.end - play.start).total_seconds()
		else:
			play.status = status
			play.start = now()

		play.save()
		frappe.db.commit()

	@reconnect_on_failure()
	def update_task(self, status, result=None, task=None):
		parsed = None
		if result:
			role, name = result.get("role"), result.get("task")
			parsed = frappe._dict(result.get("res", {}))
		else:
			role, name = task.get("role"), task.get("task")

		if not role or not name:
			return
		task_name = self.tasks[role][name]
		task = frappe.get_doc("Ansible Task", task_name)
		task.status = status

		if parsed:
			task.output = parsed.stdout
			task.error = parsed.stderr
			task.exception = parsed.msg
			# Reduce clutter be removing keys already shown elsewhere
			for key in ("stdout", "stdout_lines", "stderr", "stderr_lines", "msg"):
				result.pop(key, None)
			task.result = json.dumps(result, indent=4)
			task.end = now()
			task.duration = (task.end - task.start).total_seconds()
		else:
			task.start = now()
		task.save()
		self._publish_play_progress(task.name)
		frappe.db.commit()

	def _get_play(self):
		return self._parse_tasks(self._get_task_list())

	def _parse_tasks(self, list_tasks_output):
		"""Parse the output of ansible-playbook --list-tasks to get the play name and tasks."""
		ROLE_SEPARATOR = " : "
		TAG_SEPARATOR = "TAGS: "
		PLAY_SEPARATOR = " (all): "

		def parse_parts(line, name_separator):
			# first, second = None, None
			if name_separator in line and TAG_SEPARATOR in line:
				# Split on the first name_separator to get name
				parts = line.split(name_separator, 1)
				if len(parts) == 2:
					first = parts[0].strip()

					# Remove the TAGS part
					second_part = parts[1].strip()
					if TAG_SEPARATOR in second_part:
						second = second_part.split(TAG_SEPARATOR)[0].strip()
			return first, second

		parsed = {"name": None, "tasks": []}
		lines = list_tasks_output.strip().split("\n")

		for line in lines:
			line = line.strip()

			# Skip empty lines, playbook header and tasks header
			if not line or (line.startswith("playbook:") and line == "tasks:"):
				continue

			# Parse the play name
			if line.startswith("play #"):
				_, play = parse_parts(line, PLAY_SEPARATOR)
				if play:
					parsed["name"] = play
				continue

			# Process task lines that contain role and task information
			elif ROLE_SEPARATOR in line and TAG_SEPARATOR in line:
				role, task = parse_parts(line, ROLE_SEPARATOR)
				if role and task:
					parsed["tasks"].append({"role": role, "task": task})

		return parsed

	def _get_task_list(self):
		return subprocess.check_output(["ansible-playbook", self.playbook_path, "--list-tasks"]).decode(
			"utf-8"
		)

	def _publish_play_progress(self, task):
		frappe.publish_realtime(
			"ansible_play_progress",
			{"progress": self.task_list.index(task), "total": len(self.task_list), "play": self.play},
			doctype="Ansible Play",
			docname=self.play,
			user=frappe.session.user,
		)
