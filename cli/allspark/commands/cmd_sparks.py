import click
from allspark.core import util, logger, config


@click.group('sparks')
def cli():
    """Commands to list/add/remove sparks"""


@cli.command('list')
@click.option('--provider', prompt=config.not_set("allspark.provider"), default=config.get("allspark.provider"))
def spark_add(provider):
    provider_sparks = util.allspark_dir() + "/cli/allspark/providers/" + provider + "/sparks.json"
    provider_data = util.read_json(provider_sparks)

    logger.log("Sparks available for " + provider + " = " + str(len(provider_data['sparks'])))
    for spark in provider_data['sparks']:
        logger.log(spark['name'] + ": " + spark['description'])


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
