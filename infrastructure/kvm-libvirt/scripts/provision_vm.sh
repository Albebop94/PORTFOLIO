#!/bin/bash

# Exit on any error
set -e

VM_NAME="ubuntu-kvm-example"
VCPUS="2"
RAM_MB="2048"
DISK_SIZE="20G"
OS_VARIANT="ubuntu22.04"
IMAGE_URL="https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img"
IMAGE_DEST="/var/lib/libvirt/images/jammy-server-cloudimg-amd64.qcow2"
VM_DISK="/var/lib/libvirt/images/${VM_NAME}.qcow2"
CLOUD_INIT_ISO="/var/lib/libvirt/images/${VM_NAME}-cidata.iso"
USER_DATA_FILE="../cloud-init/user-data.yaml"

echo "Checking for base image..."
if [ ! -f "$IMAGE_DEST" ]; then
    echo "Downloading Ubuntu 22.04 Cloud Image..."
    sudo wget -qO $IMAGE_DEST $IMAGE_URL
else
    echo "Base image already exists."
fi

echo "Creating VM disk from base image..."
sudo qemu-img create -f qcow2 -b $IMAGE_DEST -F qcow2 $VM_DISK $DISK_SIZE

echo "Generating cloud-init ISO..."
# Note: requires cloud-image-utils package
sudo cloud-localds $CLOUD_INIT_ISO $USER_DATA_FILE

echo "Provisioning the VM with virt-install..."
sudo virt-install \
    --name $VM_NAME \
    --memory $RAM_MB \
    --vcpus $VCPUS \
    --disk $VM_DISK,device=disk,bus=virtio \
    --disk $CLOUD_INIT_ISO,device=cdrom \
    --os-variant $OS_VARIANT \
    --virt-type kvm \
    --graphics none \
    --network default,model=virtio \
    --import \
    --noautoconsole

echo "VM $VM_NAME provisioned successfully."
echo "Use 'virsh console $VM_NAME' to access or wait for SSH."
