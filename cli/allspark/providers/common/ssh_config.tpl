# Contents regenerated at {{data.updated_at}}

# Loop all virtual machines, linking to the bastion within the allspark network
{% for spark, data in data.sparks.iteritems() %}
# if virtual machine
Host {internal_ip or hostname}
  ProxyCommand ssh -W %h:%p {via_bastion_host_id}
  IdentityFile {internal_ssh_key}
{% endfor %}


# Loop all bastions within the allspark modules
{% for spark, data in data.sparks.iteritems() %}
# if bastion role
Host {bastion_host_x}
  Hostname {bastion_host}
  User {bastion_username}
  IdentityFile {bastion_private_key}
  ControlMaster auto
  ControlPath ~/.ssh/ansible-%r@%h:%p
  ControlPersist 5m
{% endfor %}
