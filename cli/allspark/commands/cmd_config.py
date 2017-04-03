import click
from allspark.core import logger, config


@click.group('config')
def cli():
    """Manage config to default commands"""
    pass


@cli.command('set')
@click.option('--key', prompt=True)
@click.option('--value', prompt=True)
def config_set(key, value):
    c = config.allsparkConfig()
    c.set(key, value)


@cli.command('get')
@click.option('--key', prompt=True)
def config_get(key):
    c = config.allsparkConfig()
    logger.log(c.get(key))


@cli.command('rm')
@click.option('--key', prompt=True)
def config_rm(key):
    c = config.allsparkConfig()
    c.rm(key)


@cli.command('ls')
def config_ls():
    c = config.allsparkConfig()
    c.list()
