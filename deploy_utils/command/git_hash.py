import os, re, shutil, sys

from optparse import OptionParser

from utils import system

def main():
    """
    bundle_git takes a git repo and bundles it into a zip file.
    """
    p = OptionParser("python deploy_utils git_hash [git repo] [branch]")
    p.add_option('--verbose', action='store_true', dest='verbose', help='Verbose mode')

    (options, args) = p.parse_args()
    args = args[1:]

    try:
        repo = args[0]
    except IndexError:
        p.print_usage()
        return 0

    branch = 'master' if len(args) <= 1 else args[1]
    verbose = options.verbose


    match = re.search('(.*)/(.*)(.git)', repo)
    repo_name = match.groups()[1]

    base_path = '/tmp/deployments/'
    base_repos_path = '/tmp/deployments/repos/'
    base_targets_path = '/tmp/deployments/targets/'
    repo_path = '{0}{1}'.format(base_repos_path, repo_name)
    target_path = '{0}{1}'.format(base_targets_path, repo_name)

    if not os.path.exists(base_path):
        os.mkdir(base_path)

    if not os.path.exists(base_repos_path):
        os.mkdir(base_repos_path)

    if not os.path.exists(base_targets_path):
        os.mkdir(base_targets_path)

    if not os.path.exists(repo_path):
        os.chdir(base_repos_path)
        system('git clone {0}'.format(repo), verbose=verbose)

    os.chdir(repo_path)
    system('git fetch origin', verbose=verbose)

    # TODO: check if branch exists.

    process = os.popen('cd {0} && git branch'.format(repo_path))
    branches = [ x.replace('  ', '').replace('* ', '') for x in process.read().split('\n') if x]

    if branch not in branches:
        sys.stderr.write('The branch {0} does not exist\n'.format(branch))
        return -1

    system('git checkout {0}'.format(branch), verbose=verbose)
    system('git pull origin {0}'.format(branch), verbose=verbose)

    process = os.popen('cd {0} && git rev-parse --verify HEAD'.format(repo_path))
    commit_hash = process.read().replace('\n', '')
    process.close()

    sys.stdout.write('{0}\n'.format(commit_hash))


if __name__ == '__main__':
    main()

