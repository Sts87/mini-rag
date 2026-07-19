resource "oci_artifacts_container_repository" "mini_rag_repo" {
  compartment_id = oci_identity_compartment.rag_compartment.id
  display_name   = "mini-rag-repo"
  is_immutable   = false
  is_public      = false
}