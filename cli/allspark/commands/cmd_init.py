import click
import os
import traceback
from allspark.core import config, util, logger

PROVIDERS = ['azurerm']


@click.command('init')
@click.option('--name', prompt=True)
@click.option('--provider', prompt=True, default=config.get("allspark.provider"),
              type=click.Choice(PROVIDERS))
def cli(name, provider):
    """Initiate an AllSpark Setup"""
    # remember for next time
    config.set("allspark.provider", provider)

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
            util.write_template(provider + "/main.tf.tpl", {}, project_path + "/main.tf")
            util.write_template(provider + "/variables.tf.tpl", {}, project_path + "/variables.tf")
            util.write_template(provider + "/terraform.tfvars.tpl", {}, project_path + "/terraform.tfvars")
    except Exception, err:
        logger.error("Error creating project")
        traceback.print_exc()
        util.rmdir(project_path + "/")
