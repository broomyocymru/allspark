import click
from allspark.core import util, logger


@click.command('version')
def cli():
    """Print version info, use -v for licenses"""
    logger.log("allspark Version " + util.allspark_version())

    # Output tool versions
    util.shell_run("python --version")
    util.shell_run("terraform --version")
    util.shell_run("ansible --version")

    # Output dependency licenses
    logger.vlog("OSS Licenses:")
    logger.vjson(util.oss_licenses())
