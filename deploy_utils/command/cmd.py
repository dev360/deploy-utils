import os, re, shutil, sys

from optparse import OptionParser

from fabric.api import *
from fabric.operations import put

from utils import system

def main():
    """
    cmd executes a command on multiple hosts
    """
    p = OptionParser("python deploy_utils cmd [script] --hosts=[host1,host2]]")
    p.add_option('--verbose', action='store_true', dest='verbose', help='Verbose mode')
    p.add_option('--hosts', dest='hosts', help='Hosts')
    p.add_option('--ssh_key', dest='ssh_key', help='ssh key')
    p.add_option('--ssh_user', dest='ssh_user', help='ssh user')

    (options, args) = p.parse_args()
    args = args[1:]

    script = args[0]

    if not script or not options.hosts:
        p.print_usage()
        return 0

    env.user = options.ssh_user or os.environ.get('DEPLOY_UTILS_SSH_USER') or 'root'
    env.key_filename = options.ssh_key or os.environ.get('DEPLOY_UTILS_SSH_KEY')
    #env.rootpath = '/var/apps/'
    env.hosts = (options.hosts or '').split(',')

    with settings(warn_only=True,host_string=options.hosts):
        # Create the directory if needed.
        run('{0}'.format(script))
