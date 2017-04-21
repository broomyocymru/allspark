import ctypes
import datetime
import getpass
import json
import os
import shutil
import sys
from socket import gethostname
from subprocess import Popen, PIPE, STDOUT
from pip import get_installed_distributions
import pkg_resources
from jinja2 import Environment, PackageLoader, PrefixLoader, select_autoescape
import requests
import logger, randomness
import re


def abort(msg, error_code=1):
    logger.error(msg)
    sys.exit(error_code)


def allspark_version():
    return pkg_resources.get_distribution("allspark").version


def today_string():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')


def timestamp():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def remove_non_ascii(s):
    return "".join(i for i in s if ord(i) < 128)


def shell_run(cmd, cwd=os.getcwd(), check_call=True, ctx=None, detach=False):

    stderr = STDOUT
    if detach:
        stderr = PIPE

    p = Popen(cmd, shell=True, cwd=cwd, stdin=PIPE, stdout=PIPE, stderr=stderr, universal_newlines=True)

    if not detach:
        output = ""
        while True:
            next_line = p.stdout.readline()
            output += next_line

            if next_line == "" and p.poll() is not None:
                break

            sys.stdout.write(next_line)
            sys.stdout.flush()

        if check_call and p.returncode != 0:
            logger.error("Error running '" + str(p.returncode) + "'")
            logger.error("ResultCode: " + str(p.returncode))
            sys.stdout.flush()

            if ctx is not None:
                ctx.set_return_error(True)
                if ctx.continue_processing:
                    ctx.execute_state = False

        return {"result_code": p.returncode, "std_out": output}
    else:
        return {"result_code": 0, "std_out": ""}


def is_shell_tool(name):
    """Check whether `name` is on PATH."""
    from distutils.spawn import find_executable
    return find_executable(name) is not None


def unique(seq):
    seen = set()
    for item in seq:
        if item not in seen:
            seen.add(item)
            yield item


def read_json_str(string):
    return json.loads(string)


def read_json(path):
    f = open(path, "r")
    data = json.load(f)
    f.close()
    return data


def read_file_to_str(path):
    with open(path) as f:
        data = "".join(line.rstrip() for line in f)
    return data


def write_json(path, data):
    f = open(path, "w+")
    f.write(json.dumps(data, indent=4, sort_keys=False))
    f.close()


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def get_user_name():
    return getpass.getuser()


def is_admin_shell():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin


def get_host():
    return gethostname()


def makedir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def rmdir(f):
    shutil.rmtree(f)


def write_template(template, data, output_file):
    f = open(output_file, "w+")

    loader = PrefixLoader({
        'common': PackageLoader('allspark.providers', 'common'),
        'azurerm': PackageLoader('allspark.providers', 'azurerm')
    })
    env = Environment(
        loader=loader,
        autoescape=select_autoescape(['html', 'xml'])
    )
    env.filters["replace"] = template_replace
    template = env.get_template(template)
    content = template.render(data=data)

    f.write(content)
    f.close()

def template_replace(text, name=None, data={}):
    if("<random_username>" in text):
        text = text.replace("<random_username>", randomness.username())

    if("<random_password>" in text):
        text = text.replace("<random_password>", randomness.password())

    if(name is not None and "<name>" in text):
        text = text.replace("<name>", name)

    # todo - something clever with flattening dict

    # prompted text
    if("<prompt|" in text):
        logger.log("todo - process prompt tags!")

    return text


def copy_file(current_path, local_path):
    makedir(local_path)
    shutil.copyfile(current_path, local_path)
    return


def download(url, local_file_path):
    r = requests.get(url)
    f = open(local_file_path, "w+")
    f.write(r.content)
    f.close()


def oss_licenses():
    meta_files_to_check = ['PKG-INFO', 'METADATA']
    licenses = {}

    for installed_distribution in get_installed_distributions():
        found_license = False
        for metafile in meta_files_to_check:
            if not installed_distribution.has_metadata(metafile):
                continue
            for line in installed_distribution.get_metadata_lines(metafile):
                if 'License: ' in line:
                    (k, lic) = line.split(': ', 1)

                    if lic not in licenses:
                        licenses[lic] = []
                    licenses[lic].append(installed_distribution.project_name)
                    found_license = True
        if not found_license:
            if "No License" not in licenses:
                licenses["No License"] = []
            licenses["No License"].append(installed_distribution.project_name)

    return licenses

def confirm(batch, prompt):
    if(batch):
        return True

    val = raw_input(prompt)
    return val.strip().lower() == "y"
