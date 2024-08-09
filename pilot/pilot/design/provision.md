# Provision
There's no way to do something like tofu.deploy() right now.

This goes through two levels of abstractions?. JSII

### CDKTF
We write TerraformStack subclass and define our configration in init. It should something like this
```python
from cdktf import App, Fn, TerraformStack, TerraformVariable
from cdktf_cdktf_provider_digitalocean.provider import DigitaloceanProvider
from cdktf_cdktf_provider_digitalocean.vpc import Vpc
from constructs import Construct


class MyStack(TerraformStack):
	def __init__(self, scope: Construct, id: str):
		super().__init__(scope, id)
		do_token_variable = TerraformVariable(self,"do_token", type="string")
		DigitaloceanProvider(self, "digitalocean", token=do_token_variable.string_value)
		vpc = Vpc(self, "example_vpc", name="vpc-1", region="blr-1", ip_range="ip_range")
	   
```

Unfortunately, Pilot config isn't static. But good news is, this is actually implemented as following

1. Define TerraformStack subclass, like we did before
This is equivalent of writing a HCL file

2. Define an app and call `synth` on it

```python
from cdktf import App, Fn, TerraformStack, TerraformVariable


app = App()
MyStack(app, "cdktf-demo")
app.synth()
```


3. Apply generated plan
`cdktf deploy`
We can open up the implemntation and see what happens underneath.

1. If the implementation is complicated then we can run `cdktf deploy` ourselves


---

We need to put some dynamic logic on Step 1.
We can't write a class everytime. 
Generating Python code is basically the same as writing HCL
What we can do is build a class implementation and app implementation on the fly
