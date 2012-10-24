import os, re, shutil, sys

from optparse import OptionParser

from utils import system

def main():
    """
    bundle_git takes a git repo and bundles it into a zip file.
    """
    p = OptionParser("python deploy_utils bundle_git [git repo] [branch]")
    p.add_option('--include', dest='include', help='Files to include')
    p.add_option('--verbose', action='store_true', dest='verbose', help='Verbose mode')

    (options, args) = p.parse_args()
    args = args[1:]

    try:
        repo = args[0]
    except IndexError:
        p.print_usage()
        return 0

    branch = 'master' if len(args) <= 1 else args[1]
    includes = options.include.split(',') if options.include else None
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

    if not os.path.exists(target_path):
        os.mkdir(target_path)

    target_path = target_path + '/' + commit_hash

    if os.path.exists(target_path):
        os.system('rm -rf {0}'.format(target_path))

    os.mkdir(target_path)
    os.chdir(target_path)

    if includes:
        for include in includes:
            from_path = repo_path + '/' + include
            to_path = target_path + '/' + include

            dir_path = '/'.join(include.split('/')[:-1])
            os.makedirs(dir_path)

            if os.path.isfile(from_path):
                cmd = 'cp -R {0} {1}'.format(from_path, to_path)
            else:
                cmd = 'cp -R {0} {1}'.format(from_path, '/'.join([target_path, dir_path]))

            os.system(cmd)

    else:
        from_path = repo_path + '/'
        to_path = target_path
        cmd = 'cp -R {0} {1}'.format(from_path, to_path)
        os.system(cmd)

    # Zip up the file with all the stuff in it.
    os.chdir('{0}{1}'.format(base_targets_path, repo_name))
    os.system('tar -czf {0}.tar.gz {0}/*'.format(commit_hash))

    # Delete the directory to save some space.
    os.system('rm -rf {0}'.format(target_path))
    print('{0}.tar.gz'.format(target_path))

if __name__ == '__main__':
    main()

