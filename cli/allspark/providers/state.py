from allspark.core import logger, util
import os
import traceback
import json
from datetime import datetime

class AllsparkGenerator:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.project_config = project_dir + "/allspark.json"
        self.project_infra_dir = self.project_dir + "/infrastructure"
        self.project_software_dir = self.project_dir + "/software"
        self.project_ssh_dir = self.project_dir + "/ssh"
        self.tf_outputs = "tf_out.json"

        self.data = {"provider":"", "sparks":{}}
        self.load()

    def tf_out(self):
        return util.read_json(self.project_infra_dir + "/" + self.tf_outputs)

    def vms(self):
        vms = {}
        # Get all the VPC its bastions
        for k, v in self.tf_out().iteritems():
            if k.endswith("_vm_out"):
                name = k.replace("_vm_out", "")
                ip = v['value']['private_ip']
                vms[name] = ip
        return vms

    def load(self):
        if(os.path.exists(self.project_config)):
            self.data = util.read_json(self.project_config)
        self.data['updated_at'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    def get_provider(self):
        return self.data['provider']

    def save(self):
        config_file = open(self.project_config, 'w+')
        config_file.write(json.dumps(self.data, indent=4, sort_keys=True))
        config_file.close()
        self.generate()

    def check_project_dir(self):
        if(os.path.exists(self.project_config)):
            return True
        else:
            util.abort("Error: Allspark project not found!")

    def generate_ssh_config(self):
        data = {}

        # Get all the VPC bastions
        for k, v in self.tf_out().iteritems():
            if k.endswith("_bastion"):
                vpc_name = k.replace("_bastion", "")
                vpc_bastion_ip = v['value']['bastion_ip']
                data[vpc_bastion_ip] = {
                    "name": vpc_name,
                    "username": v['value']['bastion_username'],
                    "private_ip": v['value']['bastion_private_ip'],
                    "identity_file": v['value']['identity_file'],
                    "vms": {}
                }

        # Add any VM's via the bastion
        for k, v in self.tf_out().iteritems():
            if k.endswith("_vm_out"):
                vm_name = k.replace("_vm_out", "")
                vm_private_ip = v['value']['private_ip']
                vm_bastion_ip = v['value']['bastion_ip']

                data[vm_bastion_ip]["vms"][vm_private_ip] = {
                    "username": v['value']['username'],
                    "name": vm_name
                }

        logger.vjson(data)
        util.write_template("common/ssh_config.tpl", data, self.project_software_dir + "/ssh_config.conf")

    def generate(self, provider=None):
        if(provider is None):
            provider = self.get_provider()

        try:
            if os.path.exists(self.project_dir):
                util.write_template("common/sparks.tf.tpl", self.data, self.project_infra_dir + "/sparks.tf")
                util.write_template("common/allsparks.yml.tpl", self.get_src_data(), self.project_software_dir + "/allsparks.yml")
                util.write_template("common/site.yml.tpl", self.data, self.project_software_dir + "/site.yml")

            else:
                util.makedir(self.project_dir + "/")
                self.data["provider"] = provider
                util.write_json(self.project_config, self.data)
                util.makedir(self.project_infra_dir + "/")
                util.makedir(self.project_software_dir + "/")
                util.makedir(self.project_ssh_dir + "/")
                util.shell_run("touch allspark.rsa", cwd=self.project_ssh_dir) # todo - temp workaround where terraform expects a file to exist at plan evaulation

                logger.log("init infrastructure code")
                self.generate_infra()

                logger.log("init provisioning code")
                self.generate_software()

                logger.log("complete")
        except Exception, err:
            logger.error("Error creating project")
            traceback.print_exc()

    def get_src_data(self):
        src_list = ["https://github.com/broomyocymru/allspark.common"]

        for key, value in self.data["sparks"].iteritems():
            if "software" in value:
                if "src" in value["software"]:
                    src_list.append(value["software"]["src"])

        return list(set(src_list))

    def generate_infra(self):
        provider = self.get_provider()
        util.write_template(provider + "/main.tf.tpl", {}, self.project_infra_dir + "/main.tf")
        util.write_template(provider + "/variables.tf.tpl", {}, self.project_infra_dir + "/variables.tf")
        util.write_template(provider + "/terraform.tfvars.tpl", {}, self.project_infra_dir + "/terraform.tfvars")

    def generate_software(self):
        util.write_template("common/ansible.cfg.tpl", {}, self.project_software_dir + "/ansible.cfg")
        util.download("https://raw.githubusercontent.com/broomyocymru/terraform.py/master/terraform.py", self.project_software_dir + "/inventory.py")
        util.shell_run("chmod +x inventory.py", cwd=self.project_software_dir)

    def nuke(self, force):
        util.shell_run("terraform plan -destroy", cwd=self.project_infra_dir)

        if util.confirm(force, 'Destroy Infrastructure? [Y/N] :'):
            util.shell_run("terraform destroy -force", cwd=self.project_infra_dir)

    def update(self, batch, force, apply_infra, apply_software):
        self.check_project_dir()
        self.generate()

        tf_force = " -update" if force else ""
        an_force = " --force" if force else ""

        if apply_infra and util.confirm(batch, 'Plan Infrastructure Changes [Y/N] :'):
            util.shell_run("terraform get" + tf_force, cwd=self.project_infra_dir)
            util.shell_run("terraform plan", cwd=self.project_infra_dir)

            if util.confirm(batch, 'Apply Infrastructure Changes [Y/N] :'):
                logger.log("")
                logger.log("Build Infrastructure")
                logger.log("")
                util.shell_run("terraform apply", cwd=self.project_infra_dir) # apply infra changes
                util.shell_run("terraform output -json > " + self.tf_outputs, cwd=self.project_infra_dir) # get output variables
                self.generate_ssh_config()

        # Software
        if apply_software and util.confirm(batch, 'Apply Software Changes [Y/N] :'):
            role_path = self.project_software_dir + "/roles"

            # Hack to drop/recreate roles due to ansible-galaxy bug!
            if force:
                util.shell_run("rm -r " + role_path, cwd=self.project_software_dir)

            util.shell_run("ansible-galaxy install " + an_force + " -r allsparks.yml -p " + role_path, cwd=self.project_software_dir)

            logger.log("")
            logger.log("Provision Software")
            logger.log("")
            util.shell_run("ansible -i inventory.py -m ping ssh.*", cwd=self.project_software_dir)
            #util.shell_run("ansible -i inventory.py -m win_ping winrm.*", cwd=self.project_software_dir)
            util.shell_run("ansible-playbook site.yml -i inventory.py", cwd=self.project_software_dir)

    def add(self, name, spark):
        self.check_project_dir()
        if name not in self.data["sparks"]:
            spark = self.set_placeholders(name, spark)
            self.data["sparks"][name] = spark
            self.save()
        else:
            logger.error("Spark named '" + name + "' already exists!")

    def remove(self, name):
        self.check_project_dir()
        self.data["sparks"].pop(name, "")
        self.save()

    def list(self):
        self.check_project_dir()
        return self.data["sparks"]

    def set_placeholders(self, name, spark):
        text = json.dumps(spark, indent=4, sort_keys=False)
        text = util.template_replace(text, name, spark)
        return util.read_json_str(text)
