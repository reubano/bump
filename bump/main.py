#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

""" An automated way to follow the Semantic Versioning Specification """

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

import bump

from sys import exit
from os import getcwd, path as p
from argparse import RawTextHelpFormatter, ArgumentParser

from . import Project

CURDIR = p.abspath(getcwd())

parser = ArgumentParser(
    description=(
        "description: bump makes following the Semantic Versioning"
        " Specification a breeze.\nIf called with no options, bump will print "
        "the current git repository's tag version.\nIf <dir> is not specified,"
        " the current dir is used."),
    prog='bump', usage='%(prog)s [options] <dir>',
    formatter_class=RawTextHelpFormatter)

group = parser.add_mutually_exclusive_group()

group.add_argument(
    '-t', '--type', dest='bump_type', action='store', choices=['m', 'n', 'p'],
    help=(
        "version bump type, must be one of:\n"
        "  m = major - [x].0.0\n"
        "  n = minor - x.[y].0\n"
        "  p = patch - x.y.[z]"))

group.add_argument(
    '-s', '--set', dest='version', action='store',
    help='set arbitrary version number')

parser.add_argument(
    dest='dir', nargs='?', default=CURDIR,
    help='the project directory (default: %s).\n\n' % CURDIR)

parser.add_argument(
    '-S', '--skip-commit', action='store_true', help='skip committing version'
    ' bumped files')

parser.add_argument(
    '-T', '--tag', action='store_true', help='create git tag at HEAD with the'
    ' bumped version number')

parser.add_argument(
    '-p', '--push', action='store_true', help='push to the remote origin')

parser.add_argument(
    '-a', '--stash', action='store_true', help='stash uncommitted changes')

parser.add_argument(
    '-f', '--tag-format', action='store', default=bump.DEFAULT_TAG_FMT,
    help='git tag format')

parser.add_argument(
    '-F', '--tag-msg-format', action='store', default=bump.DEFAULT_TAG_MSG_FMT,
    help='git tag message format')

parser.add_argument(
    '-c', '--commit-msg-format', action='store',
    default=bump.DEFAULT_COMMIT_MSG_FMT, help='git commit message format')

parser.add_argument(
    '-i', '--file', action='store', help='the versioned file')

parser.add_argument(
    '-v', '--version', help="Show version and exit.", action='store_true',
    default=False)

parser.add_argument(
    '-V', '--verbose', action='store_true',
    help='increase output verbosity')

args = parser.parse_args()


def run():
    project = Project(args.dir, args.file, verbose=args.verbose)

    if args.version:
        project.logger.info('bump v%s' % bump.__version__)
        exit(0)

    error = None

    if not project.version and args.bump_type:
        error = "No git tags found, please run with '-s and -T' options"
    elif (project.version and not args.bump_type and not args.version):
        error = 'Current version: %s' % project.version
    elif project.is_dirty and not args.stash:
        error = (
            "Can't bump the version with uncommitted changes. Please "
            "commit your changes or stash the following files and try "
            "again. Optionally, run with '-a' option to auto stash these "
            "files. Dirty files:\n%s" % "\n".join(project.dirty_files))
    elif project.is_dirty:
        project.logger.info("Stashing changes...\n")
        project.stash()
    elif project.version and args.bump_type:
        new_version = project.bump(args.bump_type)

        # in some cases, e.g., single file python modules, the versioned file
        # can't be predetermined and we must do a 2nd search over all files
        for wave in [1, 2]:
            project.set_versions(new_version, wave)

            if project.bumped:
                msg = 'bumped from version %s to %s'
                project.logger.info(msg, project.version, new_version)
                break
        else:
            error = "Couldn't find version '%s' in any files." % project.version
    elif args.version and not project.version_is_valid(args.version):
        error = "Invalid version: '%s'. Please use x.y.z format." % args.version
    elif args.version:
        project.set_versions(args.version)
        project.logger.info('Set to version %s' % args.version)

    if error:
        exit(error)

    if project.bumped and not args.skip_commit:
        message = args.commit_msg_format.format(version=new_version)
        project.add(project.dirty_files)
        project.commit(message)

    if project.stash_count:
        project.unstash()

    tag1 = project.bumped and project.version
    tag2 = args.version and not project.version
    tag = args.tag and (tag1 or tag2)

    if tag:
        version = (project.version or args.version)
        message = args.tag_msg_format.format(version=version)
        tag_text = args.tag_format.format(version=version)
        project.tag(message, tag_text)
    elif args.tag:
        exit("Couldn't find a version to bump. Nothing to tag.")

    if project.bumped and args.push:
        project.push()
    elif args.push:
        exit("Couldn't find a version to bump. Nothing to push.")

    exit(0)

if __name__ == "__main__":
    run()