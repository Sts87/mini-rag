#!/bin/bash
set -euo pipefail

dnf update -y

dnf install -y podman podman-compose

loginctl enable-linger opc

systemctl enable --now podman.socket || true

mkdir -p /opt/mini-rag/data/documents
mkdir -p /opt/mini-rag/data/vectorstore
mkdir -p /opt/mini-rag/data/logs

chown -R opc:opc /opt/mini-rag

echo "VM ready - Podman $(podman --version) installed"