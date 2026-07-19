variable "oci_profile" {
    type = string
}

variable "tenancy_ocid" {
    type = string
}

variable "vcn_display_name" {
    type = string
}

variable "vcn_dns_label" {
    type = string
}

variable "vcn_cidr_blocks" {
    type = list(string)
}

variable "public_subnet_dns_label" {
    type = string
}

variable "public_subnet_cidr_block" {
    type = string
}

variable "instance_shape" {
    type = string
    default = "VM.Standard.E2.1.Micro"
}

variable "instance_metadata" {
    type = map(string)
}

variable "instance_ocpus" {
    type = number
    default = 1
}

variable "instance_memory_in_gbs" {
    type = number
    default = 1
}