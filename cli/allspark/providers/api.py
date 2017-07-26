from allspark.core import logger, util
from allspark.providers import state
import pkg_resources

import os

# API Methods
CWD = state.AllsparkGenerator(os.getcwd())

# Provider Methods
def providers():
    return ['azurerm', 'aws']

# Sparks Methods
def get_sparks(provider):
    template = pkg_resources.resource_string("allspark.providers." + provider, "sparks.json")
    provider_data = util.read_json_str(template)
    return provider_data['sparks']

def available(provider):
    sparks = get_sparks(provider)
    logger.log("Sparks available for " + provider + " = " + str(len(sparks)))
    for spark in sparks:
        logger.log(spark['id'] + ": " + spark['description'])

def is_valid(name, provider):
    sparks = get_sparks(provider)
    for spark in sparks:
        if(spark['id'] == name):
            return True
    util.abort("Invalid Spark")

def get_spark(name, provider):
    sparks = get_sparks(provider)
    for spark in sparks:
        if(spark['id'] == name):
            return spark
    util.abort("Invalid Spark")

def get_provider():
    if CWD.is_project_dir():
        return CWD.get_provider()
    else:
        return None

def is_project_dir():
    return CWD.is_project_dir()

def set_spark_params(data):
    # <generate_password>
    # <prompt_input>
    return data

# Project Methods
def init(project_path, provider):
    gen = state.AllsparkGenerator(project_path)
    gen.generate(provider)

def update(cmd, dry, batch, force):
    CWD.check_project_dir()
    if cmd == "software":
        apply_infra = False
        apply_software = True
    elif cmd == "infra":
        apply_infra = True
        apply_software = False
    else:
        apply_infra = True
        apply_software = True

    if dry:
        apply_infra = False
        apply_software = False

    CWD.update(batch, force, apply_infra, apply_software)

def nuke(force):
    CWD.check_project_dir()
    CWD.nuke(force)

def add(spark, name, provider):
    CWD.check_project_dir()
    data = get_spark(spark, provider)
    data = set_spark_params(data)
    CWD.add(name, data)

def list():
    CWD.check_project_dir()
    sparks = CWD.list()
    logger.log("Sparks added to Project = " + str(len(sparks)))

    for name, config in sparks.iteritems():
        logger.log(name + ": " + config['description'])

def list_vms():
    CWD.check_project_dir()
    for name, ip in CWD.vms().iteritems():
        logger.log(name + ": " + ip)

def get_vm_ip(name):
    CWD.check_project_dir()
    vm = CWD.tf_out()[name + "_vm_out"]
    return vm['value']['private_ip']

def get_bastion_ip(name):
    CWD.check_project_dir()
    vm = CWD.tf_out()[name + "_vm_out"]
    return vm['value']['bastion_ip']

def remove(name):
    CWD.remove(name)
