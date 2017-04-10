import click
from allspark.core import util, logger
from allspark.providers import api


@click.command('nuke')
@click.option('-f', '--force', is_flag=True)
def cli(force):
    """Nuke AllSpark setup"""
    api.nuke(force)
