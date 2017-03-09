"""Setup script for AllSpark-CLI."""
from __future__ import print_function
from setuptools import setup
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
    author='Anthony Broome',
    setup_requires=['pytest-runner',],
    tests_require=['pytest',],
    install_requires=[],
    author_email='anthony.broome@capgemini.com',
    description='AllSpark CLI',
    long_description="",
    entry_points={
        'console_scripts': [
            'allspark = allspark.allspark:cli',
        ],
    },
    packages=['allspark', 'allspark.core', 'allspark.commands', 'allspark.providers'],
    include_package_data=True,
    platforms='any',
    zip_safe=False,
    package_data={
        '': ['*.json']
    },
)
