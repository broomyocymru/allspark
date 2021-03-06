import click
from allspark.core import util, logger, config
from allspark.providers import api


@click.group('sparks')
def cli():
    """Commands to list/add/remove sparks"""


@cli.command('list')
def spark_list():
    """Provides the list of configured packages"""
    api.list()


@cli.command('available')
@click.option('--provider', prompt=(not api.is_project_dir()), default=api.get_provider(), type=click.Choice(api.providers()))
def spark_list(provider):
    """Provides the list of available packages to install"""
    api.available(provider)


@cli.command('add')
@click.argument('spark')
@click.option('--name', prompt=True)
def spark_add(spark, name):
    provider = api.get_provider()
    api.is_valid(spark, provider)
    api.add(spark, name, provider)
    logger.log("Added " + spark)


@cli.command('remove')
@click.argument('name')
def spark_remove(name):
    api.remove(name)
    logger.log("Removed " + name)

#
