import os, re, shutil, sys

from optparse import OptionParser

from fabric.api import *
from fabric.operations import put

from utils import system

def main():
    """
    unzip pushes a zip file to a path on a host and unzips the contents of the file
    """
    p = OptionParser("python deploy_utils unzip [file] [destination] --hosts=[host1,host2]]")
    p.add_option('--verbose', action='store_true', dest='verbose', help='Verbose mode')
    p.add_option('--hosts', dest='hosts', help='Hosts')
    p.add_option('--ssh_key', dest='ssh_key', help='ssh key')
    p.add_option('--ssh_user', dest='ssh_user', help='ssh user')

    (options, args) = p.parse_args()
    args = args[1:]

    try:
        file_path = args[0]
        destination = args[1]
    except IndexError:
        p.print_usage()
        return 0

    if not options.hosts:
        p.print_usage()
        return 0

    env.user = options.ssh_user or os.environ.get('DEPLOY_UTILS_SSH_USER') or 'root'
    env.key_filename = options.ssh_key or os.environ.get('DEPLOY_UTILS_SSH_KEY')
    #env.rootpath = '/var/apps/'
    env.hosts = (options.hosts or '').split(',')
    #env.hosts = ['a', 'b', 'c']

    file_name = file_path.split('/')[-1:][0]

    if destination.endswith('/'):
        destination = destination[:-1]

    destination_file_name = os.path.join(destination, file_name)

    with settings(warn_only=True,host_string=options.hosts):
        # Create the directory if needed.
        run('mkdir -p {0}'.format(destination))
        put(file_path, destination)
        run('cd {0} && tar -xmzf {1}'.format(destination, destination_file_name))
        run('rm {0}'.format(destination_file_name))


