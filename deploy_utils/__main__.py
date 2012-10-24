import sys, getopt, os

from command import bundle_git, git_hash, unzip, cmd

COMMANDS = {
    'bundle_git': 'Bundles a git repo into a zip file',
    'git_hash': 'Gets the git hash for a repo and a branch',
    'unzip': 'Unzips a folder on a group of servers',
    'cmd': 'Executes a command on a group of servers',
}

def usage():
    print 'Usage: python deploy_utils [command]'
    print '\nCommands:'
    for command, description in COMMANDS.items():
        print '{0}:  {1}'.format(command.ljust(15, ' '), description)
    print '\n'

def main():
    """
    Main routine
    """
    command = sys.argv[1] if len(sys.argv) > 1 else None

    if len(sys.argv) == 1 or command not in COMMANDS:
        usage()
        return

    if command == 'bundle_git':
        bundle_git.main()
    elif command == 'git_hash':
        git_hash.main()
    elif command == 'unzip':
        unzip.main()
    elif command == 'cmd':
        cmd.main()


if __name__ == "__main__":
    main()
