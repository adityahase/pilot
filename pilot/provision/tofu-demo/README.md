# Beginning with OpenTofu
This is an attempt to learn [OpenTofu](https://github.com/opentofu/opentofu). [Terraform](https://github.com/hashicorp/terraform)'s [MPL-2.0](https://opensource.org/license/mpl-2-0) fork.

## Install

Straightforward. https://opentofu.org/docs/intro/install/deb/

## Write

Use DigitalOcean as a provider. Define a vpc, droplet, volume and a project.

Refer to `main.tf`

## Init

Init to get started. This will create a bunch of files, no need to worry about them (that are gitignored)

```sh
$ tofu init
```
```sh
Initializing the backend...

Initializing provider plugins...
- Finding digitalocean/digitalocean versions matching "~> 2.0"...
- Installing digitalocean/digitalocean v2.39.2...
- Installed digitalocean/digitalocean v2.39.2 (signed, key ID F82037E524B9C0E8)

Providers are signed by their developers.
If you'd like to know more about provider signing, you can read about it here:
https://opentofu.org/docs/cli/plugins/signing/

OpenTofu has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that OpenTofu can guarantee to make the same selections by default when
you run "tofu init" in the future.

OpenTofu has been successfully initialized!

You may now begin working with OpenTofu. Try running "tofu plan" to see
any changes that are required for your infrastructure. All OpenTofu commands
should now work.

If you ever set or change modules or backend configuration for OpenTofu,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

### Plan

Starting from an empty state (none of the resources are created). This will show what OpenTofu will do to get us to the state we've defined.

```sh
$ tofu plan
```

```sh
OpenTofu used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

OpenTofu will perform the following actions:

  # digitalocean_droplet.example_droplet will be created
  + resource "digitalocean_droplet" "example_droplet" {
      + backups              = false
      + created_at           = (known after apply)
      + disk                 = (known after apply)
      + graceful_shutdown    = false
      + id                   = (known after apply)
      + image                = "ubuntu-24-04-x64"
      + ipv4_address         = (known after apply)
      + ipv4_address_private = (known after apply)
      + ipv6                 = false
      + ipv6_address         = (known after apply)
      + locked               = (known after apply)
      + memory               = (known after apply)
      + monitoring           = false
      + name                 = "pilot-test-tofu-droplet-1"
      + price_hourly         = (known after apply)
      + price_monthly        = (known after apply)
      + private_networking   = (known after apply)
      + region               = (known after apply)
      + resize_disk          = true
      + size                 = "s-1vcpu-1gb"
      + ssh_keys             = (known after apply)
      + status               = (known after apply)
      + urn                  = (known after apply)
      + vcpus                = (known after apply)
      + volume_ids           = (known after apply)
      + vpc_uuid             = (known after apply)
    }

  # digitalocean_volume.example_volume will be created
  + resource "digitalocean_volume" "example_volume" {
      + description             = "an example volume"
      + droplet_ids             = (known after apply)
      + filesystem_label        = (known after apply)
      + filesystem_type         = (known after apply)
      + id                      = (known after apply)
      + initial_filesystem_type = "ext4"
      + name                    = "pilot-test-tofu-volume-1"
      + region                  = "blr1"
      + size                    = 10
      + urn                     = (known after apply)
    }

  # digitalocean_volume_attachment.example_volume_attachment will be created
  + resource "digitalocean_volume_attachment" "example_volume_attachment" {
      + droplet_id = (known after apply)
      + id         = (known after apply)
      + volume_id  = (known after apply)
    }

  # digitalocean_vpc.example_vpc will be created
  + resource "digitalocean_vpc" "example_vpc" {
      + created_at = (known after apply)
      + default    = (known after apply)
      + id         = (known after apply)
      + ip_range   = "10.10.10.0/24"
      + name       = "pilot-test-tofu-vpc-1"
      + region     = "blr1"
      + urn        = (known after apply)
    }

Plan: 5 to add, 0 to change, 0 to destroy.

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so OpenTofu can't guarantee to take exactly these actions if you run "tofu apply" now.
```

Note: Interactivity can be remove with `-var "do_token:<do_token>"` and `-auto-approve` (clearly dangerous).

This can also be run with

```sh
$ tofu plan -out tofu.1.plan
```
Which saves the plan to `tofu.1.plan`. We can later apply this exact plan.

```sh
Saved the plan to: tofu.1.plan

To perform exactly these actions, run the following command to apply:
    tofu apply "tofu.1.plan"

```

**TODO**: Check concurrency. Whether tofu prevents running multiple instance of `tofu plan/apply` concurrently.

### Apply 
Execute the plan and create the project, vpc, droplet and volume.
```sh
$ tofu apply
```
```sh 
OpenTofu used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

OpenTofu will perform the following actions:

  # digitalocean_droplet.example_droplet will be created
  + resource "digitalocean_droplet" "example_droplet" {
      + backups              = false
      + created_at           = (known after apply)
      + disk                 = (known after apply)
      + graceful_shutdown    = false
      + id                   = (known after apply)
      + image                = "ubuntu-24-04-x64"
      + ipv4_address         = (known after apply)
      + ipv4_address_private = (known after apply)
      + ipv6                 = false
      + ipv6_address         = (known after apply)
      + locked               = (known after apply)
      + memory               = (known after apply)
      + monitoring           = false
      + name                 = "pilot-test-tofu-droplet-1"
      + price_hourly         = (known after apply)
      + price_monthly        = (known after apply)
      + private_networking   = (known after apply)
      + region               = "blr1"
      + resize_disk          = true
      + size                 = "s-1vcpu-1gb"
      + ssh_keys             = [
          + "39020628",
        ]
      + status               = (known after apply)
      + urn                  = (known after apply)
      + vcpus                = (known after apply)
      + volume_ids           = (known after apply)
      + vpc_uuid             = (known after apply)
    }

  # digitalocean_project.example_project will be created
  + resource "digitalocean_project" "example_project" {
      + created_at  = (known after apply)
      + description = "Project for playing around with Tofu"
      + environment = "Development"
      + id          = (known after apply)
      + is_default  = false
      + name        = "Pilot Tofu Playground"
      + owner_id    = (known after apply)
      + owner_uuid  = (known after apply)
      + purpose     = "Web Application"
      + resources   = (known after apply)
      + updated_at  = (known after apply)
    }

  # digitalocean_volume.example_volume will be created
  + resource "digitalocean_volume" "example_volume" {
      + description             = "an example volume"
      + droplet_ids             = (known after apply)
      + filesystem_label        = (known after apply)
      + filesystem_type         = (known after apply)
      + id                      = (known after apply)
      + initial_filesystem_type = "ext4"
      + name                    = "pilot-test-tofu-volume-1"
      + region                  = "blr1"
      + size                    = 10
      + urn                     = (known after apply)
    }

  # digitalocean_volume_attachment.example_volume_attachment will be created
  + resource "digitalocean_volume_attachment" "example_volume_attachment" {
      + droplet_id = (known after apply)
      + id         = (known after apply)
      + volume_id  = (known after apply)
    }

  # digitalocean_vpc.example_vpc will be created
  + resource "digitalocean_vpc" "example_vpc" {
      + created_at = (known after apply)
      + default    = (known after apply)
      + id         = (known after apply)
      + ip_range   = "10.10.10.0/24"
      + name       = "pilot-test-tofu-vpc-1"
      + region     = "blr1"
      + urn        = (known after apply)
    }

Plan: 5 to add, 0 to change, 0 to destroy.
digitalocean_vpc.example_vpc: Creating...
digitalocean_volume.example_volume: Creating...
digitalocean_vpc.example_vpc: Creation complete after 2s [id=1fbcc60a-45d6-4d39-99e0-ca317348c2dc]
digitalocean_droplet.example_droplet: Creating...
digitalocean_volume.example_volume: Creation complete after 5s [id=5bc548ad-4296-11ef-8875-0a58ac14b16a]
digitalocean_droplet.example_droplet: Still creating... [10s elapsed]
digitalocean_droplet.example_droplet: Still creating... [20s elapsed]
digitalocean_droplet.example_droplet: Still creating... [30s elapsed]
digitalocean_droplet.example_droplet: Creation complete after 34s [id=432755633]
digitalocean_volume_attachment.example_volume_attachment: Creating...
digitalocean_project.example_project: Creating...
digitalocean_project.example_project: Creation complete after 4s [id=43674ed9-6aef-4bda-9050-066c472714bd]
digitalocean_volume_attachment.example_volume_attachment: Still creating... [10s elapsed]
digitalocean_volume_attachment.example_volume_attachment: Creation complete after 12s [id=432755633-5bc548ad-4296-11ef-8875-0a58ac14b16a-20240715103908703400000001]

Apply complete! Resources: 5 added, 0 changed, 0 destroyed.
```

Opentofu will maintain the state in `terraform.tfstate`.

### Destroy

Destroy will clean up the resources we created, and nothing more (hopefully).

```sh
$ tofu destroy
```
```sh
digitalocean_vpc.example_vpc: Refreshing state... [id=1fbcc60a-45d6-4d39-99e0-ca317348c2dc]
digitalocean_volume.example_volume: Refreshing state... [id=5bc548ad-4296-11ef-8875-0a58ac14b16a]
digitalocean_droplet.example_droplet: Refreshing state... [id=432755633]
digitalocean_volume_attachment.example_volume_attachment: Refreshing state... [id=432755633-5bc548ad-4296-11ef-8875-0a58ac14b16a-20240715103908703400000001]
digitalocean_project.example_project: Refreshing state... [id=43674ed9-6aef-4bda-9050-066c472714bd]

OpenTofu used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

OpenTofu will perform the following actions:

  # digitalocean_droplet.example_droplet will be destroyed
  - resource "digitalocean_droplet" "example_droplet" {
      - backups              = false -> null
      - created_at           = "2024-07-15T10:38:24Z" -> null
      - disk                 = 25 -> null
      - graceful_shutdown    = false -> null
      - id                   = "432755633" -> null
      - image                = "ubuntu-24-04-x64" -> null
      - ipv4_address         = "64.227.129.5" -> null
      - ipv4_address_private = "10.10.10.2" -> null
      - ipv6                 = false -> null
      - locked               = false -> null
      - memory               = 1024 -> null
      - monitoring           = false -> null
      - name                 = "pilot-test-tofu-droplet-1" -> null
      - price_hourly         = 0.00893 -> null
      - price_monthly        = 6 -> null
      - private_networking   = true -> null
      - region               = "blr1" -> null
      - resize_disk          = true -> null
      - size                 = "s-1vcpu-1gb" -> null
      - ssh_keys             = [
          - "39020628",
        ] -> null
      - status               = "active" -> null
      - tags                 = [] -> null
      - urn                  = "do:droplet:432755633" -> null
      - vcpus                = 1 -> null
      - volume_ids           = [
          - "5bc548ad-4296-11ef-8875-0a58ac14b16a",
        ] -> null
      - vpc_uuid             = "1fbcc60a-45d6-4d39-99e0-ca317348c2dc" -> null
    }

  # digitalocean_project.example_project will be destroyed
  - resource "digitalocean_project" "example_project" {
      - created_at  = "2024-07-15T10:38:57Z" -> null
      - description = "Project for playing around with Tofu" -> null
      - environment = "Development" -> null
      - id          = "43674ed9-6aef-4bda-9050-066c472714bd" -> null
      - is_default  = false -> null
      - name        = "Pilot Tofu Playground" -> null
      - owner_id    = 127652 -> null
      - owner_uuid  = "abbd47f101f301c9f7ab4e63c06b1b359158527f" -> null
      - purpose     = "Web Application" -> null
      - resources   = [
          - "do:droplet:432755633",
        ] -> null
      - updated_at  = "2024-07-15T10:38:57Z" -> null
    }

  # digitalocean_volume.example_volume will be destroyed
  - resource "digitalocean_volume" "example_volume" {
      - description             = "an example volume" -> null
      - droplet_ids             = [
          - 432755633,
        ] -> null
      - filesystem_type         = "ext4" -> null
      - id                      = "5bc548ad-4296-11ef-8875-0a58ac14b16a" -> null
      - initial_filesystem_type = "ext4" -> null
      - name                    = "pilot-test-tofu-volume-1" -> null
      - region                  = "blr1" -> null
      - size                    = 10 -> null
      - tags                    = [] -> null
      - urn                     = "do:volume:5bc548ad-4296-11ef-8875-0a58ac14b16a" -> null
    }

  # digitalocean_volume_attachment.example_volume_attachment will be destroyed
  - resource "digitalocean_volume_attachment" "example_volume_attachment" {
      - droplet_id = 432755633 -> null
      - id         = "432755633-5bc548ad-4296-11ef-8875-0a58ac14b16a-20240715103908703400000001" -> null
      - volume_id  = "5bc548ad-4296-11ef-8875-0a58ac14b16a" -> null
    }

  # digitalocean_vpc.example_vpc will be destroyed
  - resource "digitalocean_vpc" "example_vpc" {
      - created_at = "2024-07-15 10:38:23 +0000 UTC" -> null
      - default    = false -> null
      - id         = "1fbcc60a-45d6-4d39-99e0-ca317348c2dc" -> null
      - ip_range   = "10.10.10.0/24" -> null
      - name       = "pilot-test-tofu-vpc-1" -> null
      - region     = "blr1" -> null
      - urn        = "do:vpc:1fbcc60a-45d6-4d39-99e0-ca317348c2dc" -> null
    }

Plan: 0 to add, 0 to change, 5 to destroy.

Do you really want to destroy all resources?
  OpenTofu will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

digitalocean_volume_attachment.example_volume_attachment: Destroying... [id=432755633-5bc548ad-4296-11ef-8875-0a58ac14b16a-20240715103908703400000001]
digitalocean_project.example_project: Destroying... [id=43674ed9-6aef-4bda-9050-066c472714bd]
digitalocean_project.example_project: Destruction complete after 4s
digitalocean_volume_attachment.example_volume_attachment: Still destroying... [id=432755633-5bc548ad-4296-11ef-8875-0a58ac14b16a-20240715103908703400000001, 10s elapsed]
digitalocean_volume_attachment.example_volume_attachment: Destruction complete after 12s
digitalocean_volume.example_volume: Destroying... [id=5bc548ad-4296-11ef-8875-0a58ac14b16a]
digitalocean_droplet.example_droplet: Destroying... [id=432755633]
digitalocean_volume.example_volume: Destruction complete after 1s
digitalocean_droplet.example_droplet: Still destroying... [id=432755633, 10s elapsed]
digitalocean_droplet.example_droplet: Still destroying... [id=432755633, 20s elapsed]
digitalocean_droplet.example_droplet: Destruction complete after 23s
digitalocean_vpc.example_vpc: Destroying... [id=1fbcc60a-45d6-4d39-99e0-ca317348c2dc]
digitalocean_vpc.example_vpc: Destruction complete after 0s

Destroy complete! Resources: 5 destroyed.
```

### Done

Now you know exactly as much as I know about using OpenTofu.

Well there's the [CDK](https://github.com/hashicorp/terraform-cdk), we'll get that.
