import click
import os
from allspark.core import config, util, logger

PROVIDERS = ['azurerm']


@click.command('init')
@click.option('--name', prompt=config.not_set("allspark.name"), default=config.get("allspark.name"))
@click.option('--provider', prompt=config.not_set("allspark.provider"), default=config.get("allspark.provider"),
              type=click.Choice(PROVIDERS))
def cli(name, provider):
    """Initiate an AllSpark Setup"""
    # Create Common Project Files
    project_path = util.allspark_dir() + "/projects/" + name

    try:
        if os.path.exists(project_path):
            logger.error("Project with same name already exists!")
        else:
            util.makedir(project_path + "/")
            util.write_json(project_path + "/allspark.json", {})
            util.makedir(project_path + "/infrastructure")
            util.makedir(project_path + "/software")

            # Cloud Specific Files
            util.write_template("providers/" + name + "/main.tf.tpl", {}, project_path + "/main.tf")
            util.write_template("providers/" + name + "/variables.tf.tpl", {}, project_path + "/variables.tf")
            util.write_template("providers/" + name + "/terraform.tfvars.tpl", {}, project_path + "/terraform.tfvars")
    except:
        logger.error("Error creating project")
        util.rmdir(project_path + "/")

