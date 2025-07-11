# Download Firecracker
wget https://github.com/firecracker-microvm/firecracker/releases/download/v1.12.1/firecracker-v1.12.1-x86_64.tgz
tar -zxvf firecracker-v1.12.1-x86_64.tgz

# Copy Firecracker binaries
sudo cp release-v1.12.1-x86_64/cpu-template-helper-v1.12.1-x86_64 /usr/local/bin/cpu-template-helper
sudo cp release-v1.12.1-x86_64/firecracker-v1.12.1-x86_64 /usr/local/bin/firecracker
sudo cp release-v1.12.1-x86_64/jailer-v1.12.1-x86_64 /usr/local/bin/jailer
sudo cp release-v1.12.1-x86_64/rebase-snap-v1.12.1-x86_64 /usr/local/bin/rebase-snap
sudo cp release-v1.12.1-x86_64/seccompiler-bin-v1.12.1-x86_64 /usr/local/bin/seccompiler-bin
sudo cp release-v1.12.1-x86_64/snapshot-editor-v1.12.1-x86_64 /usr/local/bin/snapshot-editor

# Download SquashFS and Kernel
# http://spec.ccfc.min.s3.amazonaws.com/?prefix=firecracker-ci/v1.12/x86_64/vmlinux-&list-type=2
wget http://spec.ccfc.min.s3.amazonaws.com/firecracker-ci/v1.12/x86_64/vmlinux-6.1.128
# http://spec.ccfc.min.s3.amazonaws.com/?prefix=firecracker-ci/v1.12/x86_64/ubuntu-&list-type=2
wget http://spec.ccfc.min.s3.amazonaws.com/firecracker-ci/v1.12/x86_64/ubuntu-24.04.squashfs


# Prepare RootFS
unsquashfs ubuntu-24.04.squashfs
cp -v ~/.ssh/id_ed25519.pub squashfs-root/root/.ssh/authorized_keys
sudo chown -R root:root squashfs-root
truncate -s 400M ubuntu-24.04.ext4
sudo mkfs.ext4 -d squashfs-root -F ubuntu-24.04.ext4

# Move everything to downloads
mv vmlinux-6.1.128 ubuntu-24.04.squashfs ubuntu-24.04.ext4 downloads
sudo rm -rf squashfs-root

# Copy RootFS and Kernel
cp downloads/ubuntu-24.04.ext4 .
cp downloads/vmlinux-6.1.128 vmlinux.bin

# Run firecracker
rm firecracker.socket
firecracker --api-sock firecracker.socket --config-file config.json
