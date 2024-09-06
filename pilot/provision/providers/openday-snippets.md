### Start VM - boto3
```python
import boto3

client = boto3.client("ec2", region_name="ap-south-1")

instance = client.run_instances(
    ImageId="ami-00b9de22adf577ac9",
    InstanceType="t2.nano",
)
```

### Start VM - Terraform

```python
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.instance import Instance

AwsProvider(region="ap-south-1")
Instance(
    ami="ami-00b9de22adf577ac9",
    instance_type="t2.micro",
)
```
And run some magic commands

```sh
AwsProvider.synth()
tofu plan
tofu apply
```
Terraform shows us what it's going to do (truncated output)
```terraform
OpenTofu used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create

OpenTofu will perform the following actions:

  # aws_instance.compute will be created
  + resource "aws_instance" "compute" {
      + ami                                  = "ami-00b9de22adf577ac9"
      + id                                   = (known after apply)
      + instance_state                       = (known after apply)
      + instance_type                        = "t2.micro"
      + public_ip                            = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

### Resize VM - boto3
Resize however looks a little complicated. 

Stop > Wait > Resize > Start
```python
client.stop_instances(InstanceIds=[instance.id])

while client.describe_instances(InstanceIds=[instance.id]).state != "stopped":
    time.sleep(1)

client.modify_instance_attribute(
    InstanceId=instance.id,
    InstanceType={"Value": "t2.micro"},
)

client.start_instances(InstanceIds=[instance.id])
```

### Resize VM - Terraform
Looks the same as before

```python
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.instance import Instance

AwsProvider(region="ap-south-1")
Instance(
    ami="ami-00b9de22adf577ac9",
    instance_type="t2.nano",
)
```
And the same magic incantations
```sh
AwsProvider.synth()
tofu plan
tofu apply
```
And we get the same plan we'd otherwise would've executed ourselves

```terraform
OpenTofu used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  ~ update in-place

OpenTofu will perform the following actions:

  # aws_instance.compute will be updated in-place
  ~ resource "aws_instance" "compute" {
        id                                   = "i-0c73da0cfdf81dcd5"
      ~ instance_type                        = "t2.micro" -> "t2.nano"
        tags                                 = {}
        # (30 unchanged attributes hidden)

        # (8 unchanged blocks hidden)
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```

### Start VM - Terraform - DigitalOcean
```python
from cdktf_cdktf_provider_digitalocean.provider import DigitaloceanProvider
from cdktf_cdktf_provider_digitalocean.droplet import Droplet

DigitaloceanProvider()
droplet = Droplet(
    image="ubuntu-24-04-x64",
    region="blr-1",
    size="s-1vcpu-1gb",
)
```