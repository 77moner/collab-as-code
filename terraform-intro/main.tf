terraform {
  required_providers {
    local = { 
        source = "hashicorp/local"
        version = ">= 2.0"
    }
  }
}

resource "local_file" "example" {
  content  = "Managed by Terraform v2"
  filename = "${path.module}/hello.txt"
}