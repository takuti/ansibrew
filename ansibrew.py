# coding: utf-8

import click
import subprocess
import json


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        ctx.invoke(taps)
        ctx.invoke(packages)
        ctx.invoke(cask)
    else:
        ctx.invoked_subcommand


@cli.command()
def taps():
    cmd = 'brew tap'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    taps = p.communicate()[0].rstrip().split('\n')

    print('homebrew_taps:')
    for t in taps:
        print('  - %s' % t)


@cli.command()
def packages():
    cmd = 'brew list'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    installed_package_names = p.communicate()[0].rstrip().split('\n')

    installed_package_full_names = []
    depended_package_full_names = []
    options, names = {}, {}
    for name in installed_package_names:
        cmd = 'brew info --json=v1 %s' % name
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        info = p.communicate()[0].rstrip()

        # there is no information for a package
        if len(info) == 0:
            continue

        j = json.loads(info)[0]

        # get detailed information of the most stable installed version
        stable_version = j['versions']['stable']
        stable = [installed for installed in j['installed'] if installed['version'] == stable_version]

        # if there is no versions which are exactly matched to the stable version, pick one (HEAD) from installed versions
        used_options = j['installed'][0]['used_options'] if len(stable) == 0 else stable[0]['used_options']

        # remove heading '--'
        options[j['full_name']] = [opt[2:] for opt in used_options]

        depended_package_full_names += j['dependencies']
        installed_package_full_names.append(j['full_name'])
        names[j['full_name']] = j['name']

    # depended packages will be installed automatically
    print('homebrew_packages:')
    for full_name in (set(installed_package_full_names) - set(depended_package_full_names)):
        if len(options[full_name]) == 0:
            print('  - { name: %s }' % names[full_name])
        else:
            print('  - { name: %s, install_options: [%s] }' % (names[full_name], ', '.join(options[full_name])))


@cli.command()
def cask():
    cmd = 'ls /Applications'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    apps = p.communicate()[0].rstrip().split('\n')

    packages = []
    for app in apps:
        app = app.replace('.app', '')
        cmd = 'brew cask search "%s"' % app
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = p.communicate()[0].rstrip().split('\n')

        if '==> Exact match' not in res:
            continue

        packages.append(res[res.index('==> Exact match') + 1])

    print('homebrew_cask_packages:')
    for p in packages:
        print('  - { name: %s }' % p)

if __name__ == '__main__':
    cli()
