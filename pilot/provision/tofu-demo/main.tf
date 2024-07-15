terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

variable "do_token" {}

# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
}

# Create a vpc
resource "digitalocean_vpc" "example_vpc" {
  name     = "pilot-test-tofu-vpc-1"
  region   = "blr1"
  ip_range = "10.10.10.0/24"
}

# Create a droplet
resource "digitalocean_droplet" "example_droplet" {
  image  = "ubuntu-24-04-x64"
  name   = "pilot-test-tofu-droplet-1"
  region = "blr1"
  size   = "s-1vcpu-1gb"
  vpc_uuid = digitalocean_vpc.example_vpc.id
  ssh_keys = [39020628] 
  # This is my key ID. 
  # DigitalOcean doesn't let you create multiple entries with the same key
}

# Create a volume
resource "digitalocean_volume" "example_volume" {
  region                  = "blr1"
  name                    = "pilot-test-tofu-volume-1"
  size                    = 10
  initial_filesystem_type = "ext4"
  description             = "an example volume"
}

# Attach volume to the droplet
resource "digitalocean_volume_attachment" "example_volume_attachment" {
  droplet_id = digitalocean_droplet.example_droplet.id
  volume_id  = digitalocean_volume.example_volume.id
}

# Create a project
resource "digitalocean_project" "example_project" {
  name        = "Pilot Tofu Playground"
  description = "Project for playing around with Tofu"
  purpose     = "Web Application"
  environment = "Development"
  resources   = [digitalocean_droplet.example_droplet.urn]
}
