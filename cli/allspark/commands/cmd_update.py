import click
from allspark.core import util, logger
from allspark.providers import api


@click.command('update')
@click.argument('cmd', required=False)
@click.option('-d', '--dry', is_flag=True)
@click.option('-b', '--batch', is_flag=True)
@click.option('-f', '--force', is_flag=True)
def cli(cmd, dry, batch, force):
    """Update AllSpark setup"""
    api.update(cmd, dry, batch, force)
