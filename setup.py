#!/usr/bin/env python
"""
california election 2012
====

Collection of libraries and tools to processs california election data.

"""

from setuptools import setup
import election

setup(
    name='election',
    version="%d.%d.%d" % election.VERSION,
    long_description=__doc__,
    packages = ["election","election.test"],
    package_data = {'election.test': ['data/*']},
    zip_safe=True,
    license='???',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        ],
    scripts = [
        "scripts/fake_election_server",
        "scripts/fetch_and_upload_election_data", 
        ],
    install_requires = [
        'paramiko',
        'python-gflags',
        'pycurl',
        'scpclient'
        ]
)
