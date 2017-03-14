Host {allspark_admin_subnet}
  ProxyCommand ssh -W %h:%p {bastion_host}
  IdentityFile {bastion_private_key}

Host {allspark_dev_subnet}
  ProxyCommand ssh -W %h:%p {bastion_host}
  IdentityFile {bastion_private_key}

Host {allspark_prod_subnet}
  ProxyCommand ssh -W %h:%p {bastion_host}
  IdentityFile {bastion_private_key}

Host {bastion_host}
  Hostname {bastion_host}
  User {bastion_username}
  IdentityFile {bastion_private_key}
  ControlMaster auto
  ControlPath ~/.ssh/ansible-%r@%h:%p
  ControlPersist 5m
