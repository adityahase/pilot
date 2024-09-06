# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt
from typing import TYPE_CHECKING

from cdktf import Fn
from cdktf_cdktf_provider_aws.instance import Instance
from cdktf_cdktf_provider_aws.provider import AwsProvider
from constructs import Construct

if TYPE_CHECKING:
	from pilot.provision.doctype.region.region import Region
	from pilot.provision.opentofu import PilotStack


class AWS:
	def provision(self, stack: "PilotStack", scope: Construct, name: str, region: "Region") -> None:
		AwsProvider(stack, "aws", region=region.region_slug)

		Instance(
			stack,
			"compute",
			ami="ami-00b9de22adf577ac9",
			instance_type="t2.nano",
		)
