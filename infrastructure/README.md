# Infrastructure Domain

This directory contains examples of Infrastructure as Code (IaC), provisioning scripts, and automation playbooks. These examples demonstrate my expertise as a Sysadmin/DevOps engineer in automating infrastructure deployments across various environments (Cloud, Bare Metal, Virtualized).

## Directory Structure

### 1. `terraform/`
Contains Terraform configurations for provisioning resources.
- **`gcp-gke-cluster/`**: Demonstrates how to deploy a Google Kubernetes Engine (GKE) cluster in GCP using Terraform, complete with managed node pools and separate networking.
- **`proxmox-vm/`**: Demonstrates the automation of VM provisioning in a Proxmox VE environment by cloning an existing Cloud-Init template using the Telmate Proxmox provider.

### 2. `ansible/`
Contains Ansible playbooks, roles, and inventory for configuration management.
- **`inventory/`**: Sample host inventory configurations.
- **`roles/`**: Modular roles for system configuration (`common` for baseline security and packages, `docker` for installing the container engine).
- **`playbooks/`**: Entrypoint playbooks (e.g., `setup_webserver.yml`) that apply roles to target environments.

### 3. `kvm-libvirt/`
Contains bash scripts and Cloud-Init templates to provision local/bare-metal virtual machines using KVM and Libvirt.
- **`scripts/provision_vm.sh`**: A bash script using `virt-install` to automate the creation of a VM utilizing an Ubuntu cloud image.
- **`cloud-init/user-data.yaml`**: The Cloud-Init payload to bootstrap the VM with required users, SSH keys, and packages.

## Best Practices Highlighted

- **Modularity:** Terraform configurations are broken into `main`, `variables`, and `outputs`. Ansible utilizes roles for reusability.
- **Automation:** KVM provisioning removes manual ISO installations by injecting Cloud-Init data directly into cloud-ready images.
- **Security:** Examples show SSH key injection, passwordless sudo for specific users, and UFW configurations.

## Note

These are *example* configurations intended for a portfolio showcase. Before running them in a production environment, ensure you:
- Review and override the variables with your own credentials (e.g., GCP Project IDs, Proxmox API Tokens).
- Ensure required tools (`terraform`, `ansible`, `virt-install`, `cloud-image-utils`) are installed.
