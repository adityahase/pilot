#!/usr/bin/env python
from cdktf import App, Fn, TerraformStack, TerraformVariable
from cdktf_cdktf_provider_digitalocean.droplet import Droplet
from cdktf_cdktf_provider_digitalocean.project import Project
from cdktf_cdktf_provider_digitalocean.provider import DigitaloceanProvider
from cdktf_cdktf_provider_digitalocean.volume import Volume
from cdktf_cdktf_provider_digitalocean.volume_attachment import VolumeAttachment
from cdktf_cdktf_provider_digitalocean.vpc import Vpc
from constructs import Construct


class MyStack(TerraformStack):
	def __init__(self, scope: Construct, id: str):
		super().__init__(scope, id)

		region = "blr1"
		prefix = "pilot-test-tofu"
		ip_range = "10.10.10.0/24"
		image = "ubuntu-24-04-x64"
		size = "s-1vcpu-1gb"
		ssh_key_id = "39020628"  # This has to be a str because ssh_keys is Sequence[str]

		do_token_variable = TerraformVariable(
			self,
			"do_token",
			type="string",
		)
		# variable "do_token" {}

		# variable.string_value to get the actual value of the variable
		DigitaloceanProvider(self, "digitalocean", token=do_token_variable.string_value)
		# provider "digitalocean" {
		#   token = var.do_token
		# }

		vpc = Vpc(self, "example_vpc", name=f"{prefix}-vpc-1", region=region, ip_range=ip_range)
		# resource "digitalocean_vpc" "example_vpc" {
		# 	name     = "pilot-test-tofu-vpc-1"
		# 	region   = "blr1"
		# 	ip_range = "10.10.10.0/24"
		# }

		droplet = Droplet(
			self,
			"example_droplet",
			image=image,
			name=f"{prefix}-droplet-1",
			region=region,
			size=size,
			vpc_uuid=vpc.id,
			ssh_keys=[ssh_key_id],
		)
		# resource "digitalocean_droplet" "example_droplet" {
		# 	image  = "ubuntu-24-04-x64"
		# 	name   = "pilot-test-tofu-droplet-1"
		# 	region = "blr1"
		# 	size   = "s-1vcpu-1gb"
		# 	vpc_uuid = digitalocean_vpc.example_vpc.id
		# 	ssh_keys = [39020628]
		# }

		volume = Volume(
			self,
			"example_volume",
			region=region,
			name=f"{prefix}-volume-1",
			size=10,
			initial_filesystem_type="ext4",
			description="an example volume",
		)
		# resource "digitalocean_volume" "example_volume" {
		# 	region                  = "blr1"
		# 	name                    = "pilot-test-tofu-volume-1"
		# 	size                    = 10
		# 	initial_filesystem_type = "ext4"
		# 	description             = "an example volume"
		# }

		VolumeAttachment(
			self,
			"example_volume_attachment",
			droplet_id=Fn.tonumber(droplet.id),
			volume_id=volume.id,
		)
		# resource "digitalocean_volume_attachment" "example_volume_attachment" {
		# 	droplet_id = digitalocean_droplet.example_droplet.id
		# 	volume_id  = digitalocean_volume.example_volume.id
		# }

		Project(
			self,
			"example_project",
			name="Pilot Tofu Playground",
			description="Project for playing around with Tofu",
			purpose="Web Application",
			environment="Development",
			resources=[droplet.urn],
		)
		# resource "digitalocean_project" "example_project" {
		# 	name        = "Pilot Tofu Playground"
		# 	description = "Project for playing around with Tofu"
		# 	purpose     = "Web Application"
		# 	environment = "Development"
		# 	resources   = [digitalocean_droplet.example_droplet.urn]
		# }


app = App()
MyStack(app, "cdktf-demo")

app.synth()
