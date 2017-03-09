import logging
import pprint
from colorama import init, Fore
init()


def setup():
    allspark_logger = logging.getLogger('allspark-cli')
    ch = logging.StreamHandler()
    allspark_logger.addHandler(ch)

    if not hasattr(allspark_logger, 'mask_values'):
        allspark_logger.mask_values = []

    return allspark_logger


def log(msg, *args, **kwargs):
    return log_colour(msg, Fore.GREEN, *args, **kwargs)


def vlog(msg, *args, **kwargs):
    allspark_logger = logging.getLogger('allspark-cli')

    if allspark_logger.isEnabledFor(logging.DEBUG):
        return log_colour(msg, Fore.CYAN, *args, **kwargs)


def json(json):
    pp = pprint.PrettyPrinter(indent=4)
    return log(pp.pformat(json))


def vjson(json):
    allspark_logger = logging.getLogger('allspark-cli')

    if allspark_logger.isEnabledFor(logging.DEBUG):
        pp = pprint.PrettyPrinter(indent=4)
        vlog(pp.pformat(json))


def error(msg, *args, **kwargs):
    return log_colour(msg, Fore.RED, *args, **kwargs)


def warn(msg, *args, **kwargs):
    return log_colour(msg, Fore.YELLOW, *args, **kwargs)


def log_colour(msg, colour, *args, **kwargs):
    allspark_logger = logging.getLogger('allspark-cli')
    msg = str(msg)

    if allspark_logger.mask_values is not None and msg is not None:
        for to_mask in allspark_logger.mask_values:
            msg = msg.replace(to_mask, "****")

    colour_msg = colour + msg
    allspark_logger.info(colour_msg, *args, **kwargs)
    return colour_msg


def allspark(msg):
    allspark_logger = logging.getLogger('allspark-cli')
    allspark_logger.info(Fore.CYAN + msg)


def mask(val):
    allspark_logger = logging.getLogger('allspark-cli')
    allspark_logger.mask_values.append(val)


def get_masks():
    allspark_logger = logging.getLogger('allspark-cli')

    if not hasattr(allspark_logger, 'mask_values'):
        allspark_logger.mask_values = []

    return allspark_logger.mask_values


def verbose():
    allspark_logger = logging.getLogger('allspark-cli')
    return allspark_logger.isEnabledFor(logging.DEBUG)





