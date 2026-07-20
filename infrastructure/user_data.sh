#!/bin/bash
set -euo pipefail

fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' | tee -a /etc/fstab

echo 'vm.swappiness=10' | tee -a /etc/sysctl.conf
sysctl -p

dnf update -y

dnf install -y podman python3.11 python3.11-pip

python3.11 -m pip install podman-compose

echo 'export PATH=$PATH:/usr/local/bin' >> /home/opc/.bashrc

systemctl enable --now podman.socket || true

until id opc &>/dev/null; do sleep 2; done
loginctl enable-linger opc

mkdir -p /opt/mini-rag/data/documents
mkdir -p /opt/mini-rag/data/vectorstore
mkdir -p /opt/mini-rag/data/logs

chown -R opc:opc /opt/mini-rag

echo "VM ready - Podman $(podman --version) installed"