## IPv4?
### 10.0.0.0/8
Prevents Multiple VPCs from communicating. Since they share the same address space.

### 10.x.0.0/16
This is what we currently use
This gives us 256 VPCs. Seems plenty at this point. Unless we go all out on On-Premise VPCs.


That's 65k adresses per VPC. More than enough for host routing.

Not enough to give each customer / project a segment.

Let's say we cap each project to 128 addresses. That gives us 512 projects. We're already far beyond this.

Doesn't work

### Isolated
If all projects are isolated then then we can assign them the same range over and over and still be fine.


What if we assign 10.xx.xx.0/24 to each project. That gives them 256 addresses

#### VXLAN

##### Static IP - Dynamic Routing
The disovery based VXLAN was complicated since you needed to communicate node-reallocation to all neighbours.

e.g. 

nginx 10.0.0.1
app 10.0.0.2
are on 172.196.1.1

and db 10.0.0.3 is on 172.196.1.2

then we need to know 
10.0.0.1    ->  172.196.1.1
10.0.0.2    ->  172.196.1.1
10.0.0.3    ->  172.196.1.2

because of node-failure/rellocation/update this information changes then we need to update all the neighbours.


##### Dynamic IP - Static Routing
The other option is that if 

nginx 10.0.1.1 is on 172.196.1.1
app 10.0.1.2 is on 172.196.1.1
and
db 10.0.2.1 is on 172.196.1.2

then we always know
10.0.x.y is on 172.196.1.x

So our routing becomes insanely simple. The downside is that now we have to involve DNS.



### DNS Based Updates

On these two

Node Failure    ->  Reallocation
Rebalancing     ->  Reallocation 
Deploy / Update ->  Allocation / Deallocation  


## IPv6

This needs eBPF to get right. Let's not deal with it right away.
ULA?
https://en.wikipedia.org/wiki/Unique_local_address


https://community.fly.io/t/6pn-addressing-clarification/1362
https://cloud.google.com/blog/products/networking/using-ipv6-unique-local-addresses-or-ula-in-google-cloud



ULA fd00::/8
Google VPC splits this 8/40/16/32/32 Each VM gets a /96 address
