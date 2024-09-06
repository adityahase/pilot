# Cluster

## Current
Current Press clusters are simply 2m + 1 servers

1 (or 2) x Proxy
m x App
n x DB

All services are external
- Log
- Metrics
- Registry


## New

### Move Log, Metrics to inside the cluster to reduce bandwidth

For metrics this means more frequent scrape intervals would be possible

### Dynamic Ingress

Allow multiple VMs to handle Ingress simultaneously

#### S

All Non-Host Data