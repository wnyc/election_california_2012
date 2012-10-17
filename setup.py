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
    py_modules = [
        "election",
        "election/test",
        "election/test/live_server",
        ],
    packages = ["election", "election.test"],
    package_data = {'election.test': ['data/*']},
    zip_safe=True,
    license='???',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        ],
    scripts = [
        "scripts/fake_election_server",
        ],
    install_requires = [
        'python-gflags',
        ]
)
