resource "oci_core_vcn" "vcn" {
    compartment_id = oci_identity_compartment.rag_compartment.id
    
    display_name = var.vcn_display_name
    cidr_blocks   = var.vcn_cidr_blocks
    dns_label    = var.vcn_dns_label
}

resource "oci_core_internet_gateway" "internet_gateway" {
    compartment_id = oci_identity_compartment.rag_compartment.id
    vcn_id = oci_core_vcn.vcn.id

    display_name = "Internet Gateway"
    enabled = true  
}

resource "oci_core_route_table" "public_route_table" {
    compartment_id = oci_identity_compartment.rag_compartment.id
    vcn_id = oci_core_vcn.vcn.id

    display_name = "Public Route Table"
    route_rules {
        network_entity_id = oci_core_internet_gateway.internet_gateway.id
        description = "Route to Internet Gateway"
        destination = "0.0.0.0/0"
        destination_type = "CIDR_BLOCK"
    }
}

resource "oci_core_security_list" "security_list" {
    compartment_id = oci_identity_compartment.rag_compartment.id
    vcn_id = oci_core_vcn.vcn.id

    display_name = "Security List"

    egress_security_rules {
        description = "Egress rule to allow all outbound traffic"
        destination = "0.0.0.0/0"
        destination_type = "CIDR_BLOCK"
        protocol = "all"
    }

    ingress_security_rules {
        protocol = "6" 
        source = "0.0.0.0/0"
        source_type = "CIDR_BLOCK"
        tcp_options {
            min = 22
            max = 22
        }
    }

    ingress_security_rules {
        protocol = "6" 
        source = "0.0.0.0/0"
        source_type = "CIDR_BLOCK"
        tcp_options {
            min = 8501
            max = 8501
        }
    }
}

resource "oci_core_subnet" "public_subnet" {
    compartment_id = oci_identity_compartment.rag_compartment.id
    vcn_id = oci_core_vcn.vcn.id

    display_name = "Public Subnet"
    cidr_block = var.public_subnet_cidr_block
    dns_label = var.public_subnet_dns_label
    route_table_id = oci_core_route_table.public_route_table.id
    security_list_ids = [oci_core_security_list.security_list.id]
    prohibit_internet_ingress = false
    prohibit_public_ip_on_vnic = false
}