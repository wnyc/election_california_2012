#!/usr/bin/env python
"""
california election 2012
====

Collection of libraries and tools to processs california election data.

"""

from setuptools import setup
import election_parser

setup(
    name='election_parser',
    version="%d.%d.%d" % election_parser.VERSION,
    long_description=__doc__,
    packages = ["election_parser","election_parser.test"],
    package_data = {'election_parser.test': ['data/*']},
    zip_safe=True,
    license='???',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        ],
    scripts = [
        "scripts/fake_election_server",
        "scripts/fetch_parse_and_upload_election_data", 
        ],
    install_requires = [
        'paramiko',
        'python-gflags',
        'pycurl',
        'scpclient'
        ]
)
