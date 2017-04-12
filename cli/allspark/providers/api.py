from allspark.core import logger, util
from allspark.providers import state
import os

# API Methods
CWD = state.AllsparkGenerator(os.getcwd())

# Provider Methods
def providers():
    return ['azurerm']

# Sparks Methods
def get_sparks(provider):
    # todo - replace with package lookup!
    provider_sparks = util.allspark_dir() + "/cli/allspark/providers/" + provider + "/sparks.json"
    provider_data = util.read_json(provider_sparks)
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

def set_spark_params(data):
    # <generate_password>
    # <prompt_input>
    return data

# Project Methods
def init(project_path, provider):
    gen = state.AllsparkGenerator(project_path)
    gen.generate(provider)

def update(dry, batch, force):
    CWD.update(dry, batch, force)

def nuke(force):
    CWD.nuke(force)

def add(spark, name, provider):
    data = get_spark(spark, provider)
    data = set_spark_params(data)
    CWD.add(name, data)

def list():
    sparks = CWD.list()
    logger.log("Sparks added to Project = " + str(len(sparks)))

    for name, config in sparks.iteritems():
        logger.log(name + ": " + config['description'])

def list_vms():
    for name, ip in CWD.vms().iteritems():
        logger.log(name + ": " + ip)

def get_vm_ip(name):
    vm = CWD.tf_out()[name + "_vm_out"]
    return vm['value']['private_ip']

def remove(name):
    CWD.remove(name)
