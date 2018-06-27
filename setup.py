#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import sys
import ongeza as module
import pkutils

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

sys.dont_write_bytecode = True
py2_requirements = sorted(pkutils.parse_requirements('py2-requirements.txt'))
py3_requirements = sorted(pkutils.parse_requirements('requirements.txt'))
dev_requirements = sorted(pkutils.parse_requirements('dev-requirements.txt'))
dependencies = sorted(pkutils.parse_requirements('requirements.txt', dep=True))
readme = pkutils.read('README.rst')
changes = pkutils.read('CHANGES.rst').replace('.. :changelog:', '')
license = module.__license__
version = module.__version__
project = module.__title__
description = module.__description__
user = 'reubano'

# Conditional sdist dependencies:
if 'bdist_wheel' not in sys.argv and sys.version_info.major == 2:
    requirements = py2_requirements
else:
    requirements = py3_requirements

# Conditional bdist_wheel dependencies:
extras_require = sorted(set(py2_requirements).difference(py3_requirements))

setup(
    name=project,
    version=version,
    description=description,
    long_description=readme,
    author=module.__author__,
    author_email=module.__email__,
    url=pkutils.get_url(project, user),
    download_url=pkutils.get_dl_url(project, user, version),
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    package_data={},
    install_requires=requirements,
    extras_require={':python_version<"3.0"': extras_require},
    dependency_links=dependencies,
    test_suite='nose.collector',
    tests_require=dev_requirements,
    license=license,
    zip_safe=False,
    keywords=description.split(' '),
    classifiers=[
        pkutils.LICENSES[license],
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Version Control',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
    platforms=['MacOS X', 'Windows', 'Linux'],
    entry_points="""
        [console_scripts]
        ongeza=ongeza.main:run
    """
)
