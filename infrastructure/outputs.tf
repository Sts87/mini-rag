output "vm_public_ip" {
  description = "IP pública de la VM"
  value       = oci_core_instance.mini_rag_worker.public_ip
}

output "vm_ssh_command" {
  description = "Comando SSH para conectarse a la VM"
  value       = "ssh opc@${oci_core_instance.mini_rag_worker.public_ip}"
}

output "ocir_repository" {
  description = "URL del repositorio OCIR"
  value       = "scl.ocir.io/${var.tenancy_ocid}/mini-rag-repo"
}

output "app_url" {
  description = "URL de la aplicación"
  value       = "http://${oci_core_instance.mini_rag_worker.public_ip}:8501"
}