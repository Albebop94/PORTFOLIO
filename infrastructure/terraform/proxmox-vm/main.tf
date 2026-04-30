resource "proxmox_vm_qemu" "web_server" {
  name        = "ubuntu-web-${count.index + 1}"
  target_node = var.proxmox_node
  vmid        = 0 # 0 means auto-assign next available ID
  count       = var.vm_count

  # Clone from an existing template
  clone = var.template_name
  os_type = "cloud-init"

  cores   = 2
  sockets = 1
  memory  = 2048
  scsihw  = "virtio-scsi-pci"
  bootdisk = "scsi0"

  disks {
    scsi {
      scsi0 {
        disk {
          size    = "20G"
          storage = "local-lvm"
        }
      }
    }
  }

  network {
    model  = "virtio"
    bridge = "vmbr0"
  }

  lifecycle {
    ignore_changes = [
      network,
    ]
  }

  # Cloud Init Settings
  ipconfig0 = "ip=dhcp"
  ciuser    = var.ci_user
  sshkeys   = <<EOF
${var.ssh_public_key}
EOF
}
