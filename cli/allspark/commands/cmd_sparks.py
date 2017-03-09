import click
from allspark.core import util, logger


@click.group('sparks')
def cli():
    """Commands to add/remove sparks"""


@cli.command('add')
@click.argument('spark')
@click.option('--name')
@click.option('--version')
def spark_add(spark, name, version):
    logger.log("todo - spark add")


@cli.command('remove')
@click.argument('spark')
@click.option('--name')
@click.option('--version')
def spark_add(spark, name, version):
    logger.log("todo - spark remove")

