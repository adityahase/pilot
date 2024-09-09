# containerd gRPC example

This relies on https://github.com/siemens/pycontainerd
```sh
pip3 install containerd
```

```shell
sudo env/bin/python apps/pilot/containers/grpc_demo/example.py
```
You should see something like 
```shell
namespace: default
```

Note: You'll need sudo here because `/run/containerd/containerd.sock` is accessible to root. rootless containers might solve this problem, but we'll ignore that problem for now.