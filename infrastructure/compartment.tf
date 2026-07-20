resource "oci_identity_compartment" "rag_compartment" {
    compartment_id = var.tenancy_ocid
    name = "Mini-RAG"
    description = "Compartment for Mini-RAG"
    enable_delete = true
}