[ssh_connection]
ssh_args = -F ./ssh_config.conf -o ControlMaster=auto -o ControlPersist=30m
control_path = ~/.ssh/ansible-%%r@%%h:%%p
