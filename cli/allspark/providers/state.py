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

        self.data = {"provider":"", "sparks":{}}
        self.load()

    def load(self):
        if(os.path.exists(self.project_config)):
            self.data = util.read_json(self.project_config)
        self.data['updated_at'] = datetime.utcnow()

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

    def generate(self, provider=None):
        if(provider is None):
            provider = self.get_provider()

        try:
            if os.path.exists(self.project_dir):
                util.write_template("common/sparks.tf.tpl", self.data, self.project_infra_dir + "/sparks.tf")
                util.write_template("common/allsparks.yml.tpl", self.data, self.project_software_dir + "/allsparks.yml")
            else:
                util.makedir(self.project_dir + "/")
                self.data["provider"] = provider
                util.write_json(self.project_config, self.data)
                util.makedir(self.project_infra_dir + "/")
                util.makedir(self.project_software_dir + "/")
                util.makedir(self.project_ssh_dir + "/")

                logger.log("init infrastructure code")
                self.generate_infra()

                logger.log("init provisioning code")
                self.generate_software()

                logger.log("complete")
        except Exception, err:
            logger.error("Error creating project")
            traceback.print_exc()

    def generate_infra(self):
        provider = self.get_provider()
        util.write_template(provider + "/main.tf.tpl", {}, self.project_infra_dir + "/main.tf")
        util.write_template(provider + "/variables.tf.tpl", {}, self.project_infra_dir + "/variables.tf")
        util.write_template(provider + "/terraform.tfvars.tpl", {}, self.project_infra_dir + "/terraform.tfvars")

    def generate_software(self):
        util.write_template("common/ssh_config.tpl", {}, self.project_software_dir + "/ssh_config.conf")
        util.write_template("common/ansible.cfg.tpl", {}, self.project_software_dir + "/ansible.cfg")
        util.download("https://raw.githubusercontent.com/broomyocymru/terraform.py/master/terraform.py", self.project_software_dir + "/inventory.py")
        util.shell_run("chmod +x inventory.py", cwd=self.project_software_dir)

    def update(self, dry, batch, force):
        self.check_project_dir()
        self.generate()

        tf_force = " -update" if force else ""
        an_force = " -f" if force else ""


        # Download terraform and ansible modules
        util.shell_run("terraform get" + tf_force, cwd=self.project_infra_dir)

        role_path = self.project_software_dir + "/roles"
        util.shell_run("ansible-galaxy install -r allsparks.yml -p " + role_path + an_force, cwd=self.project_software_dir)

        if util.confirm(batch, 'Plan Infrastructure Changes [Y/N] :'):
            util.shell_run("terraform plan", cwd=self.project_infra_dir)

            if not dry and util.confirm(batch, 'Apply Infrastructure Changes [Y/N] :'):
                util.shell_run("terraform apply", cwd=self.project_infra_dir) # apply infra changes

                # Software
                if not dry and util.confirm(batch, 'Apply Software Changes [Y/N] :'):
                    logger.log("todo - ansible replace ping test")
                    util.shell_run("ansible -i inventory.py -m ping all", cwd=self.project_software_dir)

    def add(self, name, spark):
        self.check_project_dir()
        self.data["sparks"][name] = spark
        self.save()

    def remove(self, name):
        self.check_project_dir()
        self.data["sparks"].pop(name, "")
        self.save()

    def list(self):
        self.check_project_dir()
        return self.data["sparks"]
