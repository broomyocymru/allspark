"""Setup script for AllSpark-CLI."""
from __future__ import print_function
from setuptools import setup, find_packages
import codecs
import os
import re

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Return multiple read calls to different readable objects as a single
    string."""
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(HERE, *parts), 'r').read()


def find_version(*file_paths):
    """Find the "__version__" string in files on *file_path*."""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='allspark',
    version=find_version('allspark', '__init__.py'),
    license='MIT',
    author='Ant Broome',
    url = 'https://github.com/broomyocymru/allspark', # use the URL to the github repo
    download_url = 'https://github.com/broomyocymru/allspark/archive/' + find_version('allspark', '__init__.py') +'.tar.gz',
    setup_requires=['pytest-runner',],
    tests_require=['pytest',],
    install_requires=[
        'ansible>=2.2.1.0',
        'pywinrm>=0.2.2',
        'oauthlib>=0.7.2',
        'requests>=2.9.1',
        'requests-oauthlib>=0.5.0',
        'requests-toolbelt>=0.4.0',
        'tlslite>=0.4.8',
        'click>=6.6',
        'jsonmerge>=1.1.0',
        'jsonschema>=2.5.1',
        'vcversioner>=2.14.0.0',
        'jinja2>=2.9.5',
        'keyring>=9.0',
        'colorama>=0.3.7',
        'pyyaml>=3.12'
    ],
    author_email='broomyocymru@hotmail.com',
    description='AllSpark CLI',
    long_description="",
    entry_points={
        'console_scripts': [
            'allspark = allspark.allspark:cli',
        ],
    },
    packages=[
        'allspark',
        'allspark.core',
        'allspark.commands',
        'allspark.providers',
        'allspark.providers.azurerm',
        'allspark.provisioners.ansible'
    ],
    include_package_data=True,
    platforms='any',
    zip_safe=False,
    classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    ],
)
