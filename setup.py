# setup.py for pySerial-asyncio
#
# For Python 3.x use the corresponding Python executable,
# e.g. "python3 setup.py ..."
#
# (C) 2015-2016 Chris Liechti <cliechti@gmx.net>
#
# SPDX-License-Identifier:    BSD-3-Clause
import io
import os
import re
import sys

if sys.version_info < (3, 4):
    raise RuntimeError("pyserial-asyncio requires at least Python 3.4")

from setuptools import setup


def read(*names, **kwargs):
    """Python 2 and Python 3 compatible text file reading.

    Required for single-sourcing the version string.
    """
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    """
    Search the file for a version string.

    file_path contain string path components.

    Reads the supplied Python module as text without importing it.
    """
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = find_version('serial_asyncio', '__init__.py')


setup(
    name="pyserial-asyncio",
    description="Python Serial Port Extension - Asynchronous I/O support",
    version=version,
    author="pySerial-team",
    url="https://github.com/pyserial/pyserial-asyncio",
    packages=['serial_asyncio'],
    install_requires=[
        'pyserial',
    ],
    license="BSD",
    long_description="""\
Async I/O extension package for the Python Serial Port Extension for OSX, Linux, BSD

- Documentation: http://pyserial-asyncio.readthedocs.io
- Project Homepage: https://github.com/pyserial/pyserial-asyncio
""",
    classifiers=[
        #~ 'Development Status :: 5 - Production/Stable',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Terminals :: Serial',
    ],
    platforms='any',
)
