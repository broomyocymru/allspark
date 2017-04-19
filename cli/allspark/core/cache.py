import glob
import os
import shutil
import uuid
from os.path import expanduser

import requests
import logger


def setup():
    global session_uuid
    session_uuid = str(uuid.uuid1())


def cleanup():
    shutil.rmtree(get_cache_dir(), True)


def get_session_uuid():
    return session_uuid


def get_file(file_path):
    if file_path.startswith('http'):
        fname = file_path.split('/')[-1]
        if not os.path.exists(get_cache_dir()):
            os.makedirs(get_cache_dir())

        local_path = os.path.abspath(get_cache_dir() + '/' + fname)
        r = requests.get(file_path, stream=True)

        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            del r
        else:
            logger.error("Download failed (" + file_path + ")")

        file_path = local_path

    else:
        file_paths = glob.glob(file_path)
        if len(file_paths) > 1:
            logger.warn("More than 1 file found, taking first")

        if len(file_paths) == 0:
            logger.error("File not found (" + file_path + ")")

        file_path = os.path.abspath(file_paths[0])

    return file_path


def get_cache_dir():
    cache_dir = os.path.abspath(os.path.join(expanduser("~"), ".allspark_cache"))

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    return cache_dir
