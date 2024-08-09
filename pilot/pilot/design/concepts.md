# Concepts
---
## Global

### Region
Inter Region Latencies 
10 - 100
Maybe 300ms


### Availability Zone
< 10 ms
~3 ms

Some components are only available in the same Zone
- AWS EBS volume
- Subnet

### Node


---

## Orchestration

### Allocation
An Allocation is a mapping between a task group in a job and a client node. A single job may have hundreds or thousands of task groups, meaning an equivalent number of allocations must exist to map the work to client machines. Allocations are created by the Nomad servers as part of scheduling decisions made during an evaluation.