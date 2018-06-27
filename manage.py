#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

""" A script to manage development tasks """

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

from os import path as p
from subprocess import call, check_call, CalledProcessError
from manager import Manager

manager = Manager()
BASEDIR = p.dirname(__file__)


def upload_():
    """Upload distribution files"""
    check_call('twine upload %s' % p.join(BASEDIR, 'dist', '*'), shell=True)


def sdist_():
    """Create a source distribution package"""
    check_call(p.join(BASEDIR, 'helpers', 'srcdist'))


def wheel_():
    """Create a wheel package"""
    check_call(p.join(BASEDIR, 'helpers', 'wheel'))


def clean_():
    """Remove Python file and build artifacts"""
    check_call(p.join(BASEDIR, 'helpers', 'clean'))


@manager.command
def check():
    """Check staged changes for lint errors"""
    exit(call(p.join(BASEDIR, 'helpers', 'check-stage')))


@manager.arg('where', 'w', help='Modules to check')
@manager.arg('strict', 's', help='Check with pylint')
@manager.command
def lint(where=None, strict=False):
    """Check style with linters"""
    args = 'pylint --rcfile=tests/standard.rc -rn -fparseable ongeza'

    try:
        check_call(['flake8', where] if where else 'flake8')
        check_call(args.split(' ') + ['--py3k'])
        check_call(args.split(' ')) if strict else None
    except CalledProcessError as e:
        exit(e.returncode)


@manager.command
def pipme():
    """Install requirements.txt"""
    exit(call('pip install -r requirements.txt'.split(' ')))


@manager.command
def require():
    """Create requirements.txt"""
    cmd = 'pip freeze -l | grep -vxFf dev-requirements.txt > requirements.txt'
    exit(call(cmd, shell=True))


@manager.arg('where', 'w', help='test path', default=None)
@manager.arg(
    'stop', 'x', help='Stop after first error', type=bool, default=False)
@manager.arg('tox', 't', help='Run tox tests')
@manager.command
def test(where=None, stop=False, tox=False):
    """Run nose, tox, and script tests"""
    opts = '-xv' if stop else '-v'
    opts += 'w %s' % where if where else ''

    try:
        if tox:
            check_call('tox')
        else:
            check_call(('nosetests %s' % opts).split(' '))
            check_call(['python', p.join(BASEDIR, 'tests', 'test.py')])
    except CalledProcessError as e:
        exit(e.returncode)


@manager.command
def register():
    """Register package with PyPI"""
    exit(call('python %s register' % p.join(BASEDIR, 'setup.py'), shell=True))


@manager.command
def release():
    """Package and upload a release"""
    try:
        clean_()
        sdist_()
        wheel_()
        upload_()
    except CalledProcessError as e:
        exit(e.returncode)


@manager.command
def build():
    """Create a source distribution and wheel package"""
    try:
        clean_()
        sdist_()
        wheel_()
    except CalledProcessError as e:
        exit(e.returncode)


@manager.command
def upload():
    """Upload distribution files"""
    try:
        upload_()
    except CalledProcessError as e:
        exit(e.returncode)


@manager.command
def sdist():
    """Create a source distribution package"""
    try:
        clean_()
        sdist_()
    except CalledProcessError as e:
        exit(e.returncode)


@manager.command
def wheel():
    """Create a wheel package"""
    try:
        clean_()
        wheel_()
    except CalledProcessError as e:
        exit(e.returncode)


@manager.command
def clean():
    """Remove Python file and build artifacts"""
    try:
        clean_()
    except CalledProcessError as e:
        exit(e.returncode)

if __name__ == '__main__':
    manager.main()
