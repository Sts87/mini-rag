resource "oci_core_instance" "mini_rag_worker" {
    availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
    compartment_id = oci_identity_compartment.rag_compartment.id
    display_name = "mini-rag-worker"

    shape = var.instance_shape

    shape_config {
        ocpus = var.instance_ocpus
        memory_in_gbs = var.instance_memory_in_gbs
    } 

    create_vnic_details {
        subnet_id = oci_core_subnet.public_subnet.id
        assign_public_ip = true
        hostname_label = "mini-rag-worker"
    }


    metadata = {
        "ssh_authorized_keys" = file(pathexpand(var.instance_metadata["ssh_authorized_keys"]))
        "user_data" = base64encode(file("${path.module}/user_data.sh"))
    }

    source_details {
        source_type = "image"
        source_id = data.oci_core_images.test_images.images[0].id
        boot_volume_size_in_gbs = "50"
        boot_volume_vpus_per_gb = "20"
    }
}


data "oci_core_images" "test_images" {
  compartment_id           = var.tenancy_ocid
  operating_system         = "Oracle Linux"
  operating_system_version = "8"
  shape                    = var.instance_shape
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"
}

data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}