# Installing containerd + nerdctl
This guide installs latest versions (RC) of containerd, runc and nerdctl

https://github.com/containerd/containerd/releases/tag/v2.0.0-rc.4
https://github.com/containerd/nerdctl/releases/tag/v2.0.0-rc.1
https://github.com/opencontainers/runc/releases/tag/v1.2.0-rc.3
https://github.com/containernetworking/plugins/releases/tag/v1.5.1

#### Step 1: Installing containerd
Download https://github.com/containerd/containerd/releases/download/v2.0.0-rc.4/containerd-2.0.0-rc.4-linux-amd64.tar.gz 
```sh
wget https://github.com/containerd/containerd/releases/download/v2.0.0-rc.4/containerd-2.0.0-rc.4-linux-amd64.tar.gz
```
Extract it under `/usr/local`
```sh
sudo tar Cxzvf /usr/local containerd-2.0.0-rc.4-linux-amd64.tar.gz
```
#### Setup systemd
Download the containerd.service unit file from
https://raw.githubusercontent.com/containerd/containerd/main/containerd.service
into /etc/systemd/system/containerd.service

```shell
wget https://raw.githubusercontent.com/containerd/containerd/main/containerd.service
sudo mv containerd.service /etc/systemd/system/containerd.service
sudo systemctl daemon-reload
sudo systemctl enable --now containerd
```

#### Step 2: Installing runc

Download the `runc.amd64` binary from https://github.com/opencontainers/runc/releases/download/v1.2.0-rc.3/runc.amd64 and install it in `/usr/local/sbin`.

```shell
wget https://github.com/opencontainers/runc/releases/download/v1.2.0-rc.3/runc.amd64
```

```shell
sudo install -m 755 runc.amd64 /usr/local/sbin/runc
```

#### Step 3: Installing cni plugins
Download https://github.com/containernetworking/plugins/releases/download/v1.5.1/cni-plugins-linux-amd64-v1.5.1.tgz and extract it under `/opt/cni/bin`

```shell
wget https://github.com/containernetworking/plugins/releases/download/v1.5.1/cni-plugins-linux-amd64-v1.5.1.tgz
```

```shell
sudo mkdir -p /opt/cni/bin
sudo tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.5.1.tgz
```

#### Step 3: Installing nerdctl
Download https://github.com/containerd/nerdctl/releases/download/v2.0.0-rc.1/nerdctl-2.0.0-rc.1-linux-amd64.tar.gz and extract it under `/usr/local/bin`
```shell
wget https://github.com/containerd/nerdctl/releases/download/v2.0.0-rc.1/nerdctl-2.0.0-rc.1-linux-amd64.tar.gz
```

```shell
sudo tar Cxzvf /usr/local/bin nerdctl-2.0.0-rc.1-linux-amd64.tar.gz
```
