# Beginning with CDKTF
Cloud Development Kit with Terraform

## Install
Install CDKTF with NPM

```sh
$ npm install --global cdktf-cli@latest
```

Also needs `pipenv`

```sh
pip install pipenv
```

Reference: https://developer.hashicorp.com/terraform/tutorials/cdktf/cdktf-install?variants=cdk-language%3Apython

## Initialize

Initialize project directory
```sh
$ mkdir cdktf-demo 
$ cd cdktf-demo
$ cdktf init --template=python --local --providers=digitalocean/digitalocean
```

```
[2024-07-15T17:18:33.723] [INFO] default - Unable to determine Terraform version: Error: Terraform CLI not present - Please install a current version https://learn.hashicorp.com/terraform/getting-started/install.html
Note: By supplying '--local' option you have chosen local storage mode for storing the state of your stack.
This means that your Terraform state file will be stored locally on disk in a file 'terraform.<STACK NAME>.tfstate' in the root of your project.
[2024-07-15T17:18:33.782] [INFO] default - Unable to determine Terraform version: Error: Terraform CLI not present - Please install a current version https://learn.hashicorp.com/terraform/getting-started/install.html
? Project Name cdktf-demo
? Project Description A simple getting started project for cdktf.
? Do you want to send crash reports to the CDKTF team? Refer to https://developer.hashicorp.com/terraform/cdktf/create-and-deploy/configuration-file#enable-crash-reporting-for-the-cli for more information no
Courtesy Notice: Pipenv found itself running within a virtual environment, so it will automatically use that environment, instead of creating its own for any project. You can set PIPENV_IGNORE_VIRTUALENVS=1 to force pipenv to ignore that environment and create its own instead. You can set PIPENV_VERBOSITY=-1 to suppress this warning.
Pipfile.lock not found, creating...
Locking [packages] dependencies...
Locking [dev-packages] dependencies...
Updated Pipfile.lock (4e61a4ba9e6f02f50f68627253af5ababd9b1b4c1e10294e48158e1f42c0c5a6)!
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
Installing dependencies from Pipfile.lock (c0c5a6)...
Courtesy Notice: Pipenv found itself running within a virtual environment, so it will automatically use that environment, instead of creating its own for any project. You can set PIPENV_IGNORE_VIRTUALENVS=1 to force pipenv to ignore that environment and create its own instead. You can set PIPENV_VERBOSITY=-1 to suppress this warning.
Installing cdktf~=0.20.8...
Resolving cdktf~=0.20.8...
Added cdktf to Pipfile's [packages] ...
✔ Installation Succeeded
Pipfile.lock (c0c5a6) out of date: run `pipfile lock` to update to (813b71)...
Running $ pipenv lock then $ pipenv sync.
Locking [packages] dependencies...
Building requirements...
Resolving dependencies...
✔ Success!
Locking [dev-packages] dependencies...
Updated Pipfile.lock (7f87fbbb4630d4c1d03d4ec00579a88eb8c446f6f67d713759079ac767813b71)!
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
Installing dependencies from Pipfile.lock (813b71)...
All dependencies are now up-to-date!
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
Installing dependencies from Pipfile.lock (813b71)...
Courtesy Notice: Pipenv found itself running within a virtual environment, so it will automatically use that environment, instead of creating its own for any project. You can set PIPENV_IGNORE_VIRTUALENVS=1 to force pipenv to ignore that environment and create its own instead. You can set PIPENV_VERBOSITY=-1 to suppress this warning.
Installing pytest...
Resolving pytest...
Added pytest to Pipfile's [packages] ...
✔ Installation Succeeded
Pipfile.lock (813b71) out of date: run `pipfile lock` to update to (4b37ac)...
Running $ pipenv lock then $ pipenv sync.
Locking [packages] dependencies...
Building requirements...
Resolving dependencies...
✔ Success!
Locking [dev-packages] dependencies...
Updated Pipfile.lock (bcd1e1ca83ad80fd3a755c93c9b682c802732ef5d3bcf812b41a76b3944b37ac)!
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
Installing dependencies from Pipfile.lock (4b37ac)...
All dependencies are now up-to-date!
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
Installing dependencies from Pipfile.lock (4b37ac)...
========================================================================================================

  Your cdktf Python project is ready!

  cat help                Prints this message

  Compile:
    pipenv run ./main.py  Compile and run the python code.

  Synthesize:
    cdktf synth [stack]   Synthesize Terraform resources to cdktf.out/

  Diff:
    cdktf diff [stack]    Perform a diff (terraform plan) for the given stack

  Deploy:
    cdktf deploy [stack]  Deploy the given stack

  Destroy:
    cdktf destroy [stack] Destroy the given stack

  Learn more about using modules and providers https://cdk.tf/modules-and-providers

Use Providers:

  You can add prebuilt providers (if available) or locally generated ones using the add command:
  
  cdktf provider add "aws@~>3.0" null kreuzwerker/docker

  You can find all prebuilt providers on PyPI: https://pypi.org/user/cdktf-team/
  You can also install these providers directly through pipenv:

  pipenv install cdktf-cdktf-provider-aws
  pipenv install cdktf-cdktf-provider-google
  pipenv install cdktf-cdktf-provider-azurerm
  pipenv install cdktf-cdktf-provider-docker
  pipenv install cdktf-cdktf-provider-github
  pipenv install cdktf-cdktf-provider-null

  You can also build any module or provider locally. Learn more: https://cdk.tf/modules-and-providers

========================================================================================================
[2024-07-15T17:18:57.287] [INFO] default - Checking whether pre-built provider exists for the following constraints:
  provider: digitalocean/digitalocean
  version : latest
  language: python
  cdktf   : 0.20.8

[2024-07-15T17:19:05.780] [INFO] default - Found pre-built provider.
Installing package cdktf-cdktf-provider-digitalocean @ 11.5.2 using pipenv.
Installing cdktf-cdktf-provider-digitalocean~=11.5.2...
Resolving cdktf-cdktf-provider-digitalocean~=11.5.2...
Added cdktf-cdktf-provider-digitalocean to Pipfile's [packages] ...
✔ Installation Succeeded
Pipfile.lock (4b37ac) out of date: run `pipfile lock` to update to (10ade4)...
Running $ pipenv lock then $ pipenv sync.
Locking [packages] dependencies...
Building requirements...
Resolving dependencies...
✔ Success!
Locking [dev-packages] dependencies...
Updated Pipfile.lock (034b60286cee8ece9a70b1f6be878fce1d98fd02f968070932a3a72f8810ade4)!
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
Installing dependencies from Pipfile.lock (10ade4)...
All dependencies are now up-to-date!
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
Installing dependencies from Pipfile.lock (10ade4)...
Package installed.
```


## Write

Refer to `main.py`

This is equivalent of writing a HCL file

Few quirks
- Typecasts
  - `Droplet.ssh_keys` expects `Sequence[str]`. HCL file implies `int`
  - `Fn.tonumber`
  - `Droplet.id` is a `str`, `VolumeAttachment.droplet_id` exepect an `int`
- Variables
  - `variable.string_value` to actually access the value
## Debug
```sh
$ cdktf debug
```
```
cdktf debug
language: python
cdktf-cli: 0.20.8
node: v18.12.1
cdktf: 0.20.8
constructs: 10.3.0
jsii: 1.101.0
terraform: Error: Usage Error: Unknown: Error loading terraform version Error: spawn terraform ENOENT
arch: x64
os: linux 6.9.9-060909-generic
python: Python 3.12.4
pip: pip 24.1.2 from /home/aditya/Frappe/benches/pilot/env/lib/python3.12/site-packages/pip (python 3.12)
pipenv: pipenv, version 2024.0.1
providers
cdktf-cdktf-provider-digitalocean (PREBUILT)
        terraform provider version: 2.39.2 
        prebuilt provider version: 11.5.2
        cdktf version: ^0.20.0
```

We haven't install terraform. Need to tell cdktf to use tofu binary with

```sh
export TERRAFORM_BINARY_NAME=tofu
```
Now CDKTF should work fine
```
...
terraform: 1.7.3
...
```

Without this `plan` will fail with `execvp(3) failed.: No such file or directory`

## Plan
This is more or less like `tofu plan`

**Note**: Need to pass `do_token` with `--var "do_token=<do_token>"`
```sh
$ cdktf plan
```
```
⠇  Synthesizing
cdktf-demo  Initializing the backend...
cdktf-demo  Initializing provider plugins...
            - Reusing previous version of digitalocean/digitalocean from the dependency lock file
cdktf-demo  - Using previously-installed digitalocean/digitalocean v2.39.2

            OpenTofu has been successfully initialized!
            
            You may now begin working with OpenTofu. Try running "tofu plan" to see
            any changes that are required for your infrastructure. All OpenTofu commands
            should now work.

            If you ever set or change modules or backend configuration for OpenTofu,
            rerun this command to reinitialize your working directory. If you forget, other
            commands will detect it and remind you to do so if necessary.
cdktf-demo  - Fetching digitalocean/digitalocean 2.39.2 for linux_amd64...
cdktf-demo  - Retrieved digitalocean/digitalocean 2.39.2 for linux_amd64 (signed, key ID F82037E524B9C0E8)
            - Obtained digitalocean/digitalocean checksums for linux_amd64; All checksums for this platform were already tracked in the lock file
cdktf-demo  Success! OpenTofu has validated the lock file and found no need for changes.
cdktf-demo  OpenTofu used the selected providers to generate the following execution
            plan. Resource actions are indicated with the following symbols:
              + create

            OpenTofu will perform the following actions:
cdktf-demo    # digitalocean_droplet.example_droplet (example_droplet) will be created
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

              # digitalocean_project.example_project (example_project) will be created
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

              # digitalocean_volume.example_volume (example_volume) will be created
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

              # digitalocean_volume_attachment.example_volume_attachment (example_volume_attachment) will be created
              + resource "digitalocean_volume_attachment" "example_volume_attachment" {
                  + droplet_id = (known after apply)
                  + id         = (known after apply)
                  + volume_id  = (known after apply)
                }

              # digitalocean_vpc.example_vpc (example_vpc) will be created
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
            
            ─────────────────────────────────────────────────────────────────────────────

            Saved the plan to: plan

            To perform exactly these actions, run the following command to apply:
                tofu apply "plan"
```


## Deploy
Same as `tofu apply`. This handles dependencies across multiple stacks, whatever that means.
```sh
$ cdktf deploy
```
```
⠦  Synthesizing
cdktf-demo  Initializing the backend...
cdktf-demo  Initializing provider plugins...
            - Reusing previous version of digitalocean/digitalocean from the dependency lock file
cdktf-demo  - Using previously-installed digitalocean/digitalocean v2.39.2

            OpenTofu has been successfully initialized!
            
            You may now begin working with OpenTofu. Try running "tofu plan" to see
            any changes that are required for your infrastructure. All OpenTofu commands
            should now work.

            If you ever set or change modules or backend configuration for OpenTofu,
            rerun this command to reinitialize your working directory. If you forget, other
            commands will detect it and remind you to do so if necessary.
cdktf-demo  - Fetching digitalocean/digitalocean 2.39.2 for linux_amd64...
cdktf-demo  - Retrieved digitalocean/digitalocean 2.39.2 for linux_amd64 (signed, key ID F82037E524B9C0E8)
            - Obtained digitalocean/digitalocean checksums for linux_amd64; All checksums for this platform were already tracked in the lock file
cdktf-demo  Success! OpenTofu has validated the lock file and found no need for changes.
cdktf-demo  OpenTofu used the selected providers to generate the following execution plan.
            Resource actions are indicated with the following symbols:
              + create

            OpenTofu will perform the following actions:
cdktf-demo    # digitalocean_droplet.example_droplet (example_droplet) will be created
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

              # digitalocean_project.example_project (example_project) will be created
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

              # digitalocean_volume.example_volume (example_volume) will be created
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

              # digitalocean_volume_attachment.example_volume_attachment (example_volume_attachment) will be created
              + resource "digitalocean_volume_attachment" "example_volume_attachment" {
                  + droplet_id = (known after apply)
                  + id         = (known after apply)
                  + volume_id  = (known after apply)
                }

              # digitalocean_vpc.example_vpc (example_vpc) will be created
              + resource "digitalocean_vpc" "example_vpc" {
                  + created_at = (known after apply)
                  + default    = (known after apply)
                  + id         = (known after apply)
                  + ip_range   = "10.10.10.0/24"
cdktf-demo  + name       = "pilot-test-tofu-vpc-1"
                  + region     = "blr1"
                  + urn        = (known after apply)
                }

            Plan: 5 to add, 0 to change, 0 to destroy.
            
            Do you want to perform these actions?
              OpenTofu will perform the actions described above.
              Only 'yes' will be accepted to approve.
cdktf-demo  Enter a value: yes
cdktf-demo  digitalocean_vpc.example_vpc: Creating...
cdktf-demo  digitalocean_volume.example_volume: Creating...
cdktf-demo  digitalocean_vpc.example_vpc: Creation complete after 4s [id=a2efcafc-c36e-4dc6-b0a0-05168c64e035]
cdktf-demo  digitalocean_droplet.example_droplet: Creating...
cdktf-demo  digitalocean_volume.example_volume: Creation complete after 6s [id=6ca3afb6-4363-11ef-8e54-0a58ac14b334]
cdktf-demo  digitalocean_droplet.example_droplet: Still creating... [10s elapsed]
cdktf-demo  digitalocean_droplet.example_droplet: Still creating... [20s elapsed]
cdktf-demo  digitalocean_droplet.example_droplet: Still creating... [30s elapsed]
cdktf-demo  digitalocean_droplet.example_droplet: Creation complete after 33s [id=433003236]
cdktf-demo  digitalocean_volume_attachment.example_volume_attachment: Creating...
cdktf-demo  digitalocean_project.example_project: Creating...
cdktf-demo  digitalocean_project.example_project: Creation complete after 4s [id=883b0f81-94e0-4d25-a414-8c4ba59dc2ad]
cdktf-demo  digitalocean_volume_attachment.example_volume_attachment: Still creating... [10s elapsed]
cdktf-demo  digitalocean_volume_attachment.example_volume_attachment: Creation complete after 13s [id=433003236-6ca3afb6-4363-11ef-8e54-0a58ac14b334-20240716110706136600000001]
cdktf-demo  
            Apply complete! Resources: 5 added, 0 changed, 0 destroyed.

No outputs found.
```

## Destroy
```sh
$ cdktf destroy
```
```sh
⠇  Synthesizing
cdktf-demo  Initializing the backend...
cdktf-demo  Initializing provider plugins...
            - Reusing previous version of digitalocean/digitalocean from the dependency lock file
cdktf-demo  - Using previously-installed digitalocean/digitalocean v2.39.2

            OpenTofu has been successfully initialized!
            
            You may now begin working with OpenTofu. Try running "tofu plan" to see
            any changes that are required for your infrastructure. All OpenTofu commands
            should now work.

            If you ever set or change modules or backend configuration for OpenTofu,
            rerun this command to reinitialize your working directory. If you forget, other
            commands will detect it and remind you to do so if necessary.
cdktf-demo  - Fetching digitalocean/digitalocean 2.39.2 for linux_amd64...
cdktf-demo  - Retrieved digitalocean/digitalocean 2.39.2 for linux_amd64 (signed, key ID F82037E524B9C0E8)
            - Obtained digitalocean/digitalocean checksums for linux_amd64; All checksums for this platform were already tracked in the lock file
cdktf-demo  Success! OpenTofu has validated the lock file and found no need for changes.
cdktf-demo  digitalocean_vpc.example_vpc: Refreshing state... [id=a2efcafc-c36e-4dc6-b0a0-05168c64e035]
cdktf-demo  digitalocean_volume.example_volume: Refreshing state... [id=6ca3afb6-4363-11ef-8e54-0a58ac14b334]
cdktf-demo  digitalocean_droplet.example_droplet: Refreshing state... [id=433003236]
cdktf-demo  digitalocean_volume_attachment.example_volume_attachment: Refreshing state... [id=433003236-6ca3afb6-4363-11ef-8e54-0a58ac14b334-20240716110706136600000001]
cdktf-demo  digitalocean_project.example_project: Refreshing state... [id=883b0f81-94e0-4d25-a414-8c4ba59dc2ad]
cdktf-demo  OpenTofu used the selected providers to generate the following execution plan.
            Resource actions are indicated with the following symbols:
              - destroy

            OpenTofu will perform the following actions:
cdktf-demo    # digitalocean_droplet.example_droplet (example_droplet) will be destroyed
              - resource "digitalocean_droplet" "example_droplet" {
                  - backups              = false -> null
                  - created_at           = "2024-07-16T11:06:20Z" -> null
                  - disk                 = 25 -> null
                  - graceful_shutdown    = false -> null
                  - id                   = "433003236" -> null
                  - image                = "ubuntu-24-04-x64" -> null
                  - ipv4_address         = "159.65.149.187" -> null
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
                  - urn                  = "do:droplet:433003236" -> null
                  - vcpus                = 1 -> null
                  - volume_ids           = [
                      - "6ca3afb6-4363-11ef-8e54-0a58ac14b334",
                    ] -> null
                  - vpc_uuid             = "a2efcafc-c36e-4dc6-b0a0-05168c64e035" -> null
                }

              # digitalocean_project.example_project (example_project) will be destroyed
              - resource "digitalocean_project" "example_project" {
                  - created_at  = "2024-07-16T11:06:53Z" -> null
                  - description = "Project for playing around with Tofu" -> null
                  - environment = "Development" -> null
                  - id          = "883b0f81-94e0-4d25-a414-8c4ba59dc2ad" -> null
                  - is_default  = false -> null
                  - name        = "Pilot Tofu Playground" -> null
                  - owner_id    = 127652 -> null
                  - owner_uuid  = "abbd47f101f301c9f7ab4e63c06b1b359158527f" -> null
                  - purpose     = "Web Application" -> null
                  - resources   = [
                      - "do:droplet:433003236",
                    ] -> null
                  - updated_at  = "2024-07-16T11:06:53Z" -> null
                }

              # digitalocean_volume.example_volume (example_volume) will be destroyed
              - resource "digitalocean_volume" "example_volume" {
                  - description             = "an example volume" -> null
                  - droplet_ids             = [
                      - 433003236,
                    ] -> null
                  - filesystem_type         = "ext4" -> null
                  - id                      = "6ca3afb6-4363-11ef-8e54-0a58ac14b334" -> null
                  - initial_filesystem_type = "ext4" -> null
                  - name                    = "pilot-test-tofu-volume-1" -> null
cdktf-demo  - region                  = "blr1" -> null
                  - size                    = 10 -> null
                  - tags                    = [] -> null
                  - urn                     = "do:volume:6ca3afb6-4363-11ef-8e54-0a58ac14b334" -> null
                }

              # digitalocean_volume_attachment.example_volume_attachment (example_volume_attachment) will be destroyed
              - resource "digitalocean_volume_attachment" "example_volume_attachment" {
                  - droplet_id = 433003236 -> null
                  - id         = "433003236-6ca3afb6-4363-11ef-8e54-0a58ac14b334-20240716110706136600000001" -> null
                  - volume_id  = "6ca3afb6-4363-11ef-8e54-0a58ac14b334" -> null
                }

              # digitalocean_vpc.example_vpc (example_vpc) will be destroyed
              - resource "digitalocean_vpc" "example_vpc" {
                  - created_at = "2024-07-16 11:06:17 +0000 UTC" -> null
                  - default    = false -> null
                  - id         = "a2efcafc-c36e-4dc6-b0a0-05168c64e035" -> null
                  - ip_range   = "10.10.10.0/24" -> null
                  - name       = "pilot-test-tofu-vpc-1" -> null
                  - region     = "blr1" -> null
                  - urn        = "do:vpc:a2efcafc-c36e-4dc6-b0a0-05168c64e035" -> null
                }

            Plan: 0 to add, 0 to change, 5 to destroy.
            
            Do you really want to destroy all resources?
              OpenTofu will destroy all your managed infrastructure, as shown above.
              There is no undo. Only 'yes' will be accepted to confirm.
cdktf-demo  Enter a value: yes
cdktf-demo  digitalocean_volume_attachment.example_volume_attachment: Destroying... [id=433003236-6ca3afb6-4363-11ef-8e54-0a58ac14b334-20240716110706136600000001]
cdktf-demo  digitalocean_project.example_project: Destroying... [id=883b0f81-94e0-4d25-a414-8c4ba59dc2ad]
cdktf-demo  digitalocean_project.example_project: Destruction complete after 3s
cdktf-demo  digitalocean_volume_attachment.example_volume_attachment: Still destroying... [id=433003236-6ca3afb6-4363-11ef-8e54-0a58ac14b334-20240716110706136600000001, 10s elapsed]
cdktf-demo  digitalocean_volume_attachment.example_volume_attachment: Destruction complete after 13s
cdktf-demo  digitalocean_volume.example_volume: Destroying... [id=6ca3afb6-4363-11ef-8e54-0a58ac14b334]
            digitalocean_droplet.example_droplet: Destroying... [id=433003236]
cdktf-demo  digitalocean_volume.example_volume: Destruction complete after 1s
cdktf-demo  digitalocean_droplet.example_droplet: Still destroying... [id=433003236, 10s elapsed]
cdktf-demo  digitalocean_droplet.example_droplet: Still destroying... [id=433003236, 20s elapsed]
cdktf-demo  digitalocean_droplet.example_droplet: Destruction complete after 23s
cdktf-demo  digitalocean_vpc.example_vpc: Destroying... [id=a2efcafc-c36e-4dc6-b0a0-05168c64e035]
cdktf-demo  digitalocean_vpc.example_vpc: Destruction complete after 1s
cdktf-demo  
            Destroy complete! Resources: 5 destroyed.
```

## Done
Now you know everything I know about CDKTF

We're still aren't very far from HCLs. 

We don't have to convert Documents to HCL. But the actual superpower will be to call `plan/deploy/destroy` from Python.

We can probably get the equivalent of `cdktf deploy` with some hacks around TerraformCli and jsii 
References: 
- https://github.com/hashicorp/terraform-cdk/blob/40a1a39a4655720aec8f1bdb93dd9689f6747fa5/packages/%40cdktf/cli-core/src/lib/models/terraform.ts

- https://github.com/hashicorp/terraform-cdk/issues/237#issuecomment-864523914