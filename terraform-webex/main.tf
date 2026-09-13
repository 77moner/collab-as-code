terraform {
  required_providers {
    webex = {
      source = "Nathan-Loisel/webex"
    }
  }
}

provider "webex" {
  # token pulled from WEBEX_TOKEN environment variable
}

data "webex_workspaces" "all" {
  # no filters, get all workspaces
}

output "workspace_names" {
  value = [for w in data.webex_workspaces.all.workspaces : w.display_name]
}