terraform {
    required_providers {
        oci = {
            source = "oracle/oci"
        }
    }
}

provider "oci" {
    config_file_profile = var.oci_profile
}

