import click
from allspark.core import util, logger, config
from allspark.providers import api


@click.group('sparks')
def cli():
    """Commands to list/add/remove sparks"""


@cli.command('list')
@click.option('--provider', prompt=config.not_set("allspark.provider"), default=config.get("allspark.provider"))
def spark_list(provider):
    api.list_sparks(provider)


@cli.command('add')
@click.argument('spark')
@click.option('--name', prompt=True)
@click.option('--provider', prompt=config.not_set("allspark.provider"), default=config.get("allspark.provider"))
def spark_add(spark, name, provider):
    api.is_valid(spark, provider)
    api.add(spark, name, provider)
    logger.log("Added " + spark)


@cli.command('remove')
@click.argument('name')
def spark_remove(name):
    api.remove(name)
    logger.log("Removed " + name)

#
