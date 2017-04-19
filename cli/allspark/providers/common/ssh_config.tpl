# Contents regenerated at {{data.updated_at}}
{% for bastion_ip, bastion_details in data.iteritems() %}
{% for vm_private_ip, vm_details in bastion_details['vms'].iteritems() %}
# {{vm_details['name']}}
Host {{vm_private_ip}}
  ProxyJump {{bastion_details['username']}}@{{bastion_details['private_ip']}}:22
  User {{vm_details['username']}}
  IdentityFile {{bastion_details['identity_file']}}
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
{% endfor %}

# Bastion {{bastion_details['bastion_private_ip']}}
Host {{bastion_details['private_ip']}}
  Hostname {{bastion_ip}}
  User {{bastion_details['username']}}
  IdentityFile {{bastion_details['identity_file']}}
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
  ControlMaster auto
  ControlPath ~/.ssh/%%h-%%r
  ControlPersist 5m
  ForwardAgent yes
{% endfor %}
