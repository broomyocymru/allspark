import click
import os
from allspark.core import config, util, logger
from allspark.providers import api

@click.command('dev')
def cli():
    result = util.template_replace("<prompt msg='test'/> <prompt msg='test2'/>")
    logger.log(result)
