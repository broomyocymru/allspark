from allspark.core import logger, util
from allspark.providers import state
import os

# API Methods

# Provider Methods
def providers():
    return ['azurerm']

# Sparks Methods
def get_sparks(provider):
    # todo - replace with package lookup!
    provider_sparks = util.allspark_dir() + "/cli/allspark/providers/" + provider + "/sparks.json"
    provider_data = util.read_json(provider_sparks)
    return provider_data['sparks']

def list_sparks(provider):
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

# Project Methods
def init(project_path, provider):
    gen = state.AllsparkGenerator(project_path)
    gen.generate(provider)

def update(dry, batch):
    gen = state.AllsparkGenerator(os.getcwd())
    gen.update(dry, batch)

def add(spark, name, provider):
    gen = state.AllsparkGenerator(os.getcwd())
    data = get_spark(spark, provider)
    gen.add(name, data)

def remove(name):
    gen = state.AllsparkGenerator(os.getcwd())
    gen.remove(name)
