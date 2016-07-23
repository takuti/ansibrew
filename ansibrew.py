# coding: utf-8

import yaml
import click
import subprocess


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    ctx.invoked_subcommand


@cli.command()
def taps():
    cmd = 'brew tap'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    taps = p.communicate()[0].rstrip().split('\n')
    var = {'homebrew_taps': taps}

    print(yaml.dump(var, default_flow_style=False))


@cli.command()
def packages():
    cmd = 'brew list'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    packages = p.communicate()[0].rstrip().split('\n')

    excepted_packages = []
    for package in packages:
        cmd = 'brew info %s' % package
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        info = p.communicate()[0].rstrip().split('\n')

        if '==> Dependencies' not in info:
            continue

        parsed_required = info[info.index('==> Dependencies') + 1].split(' ')
        excepted_packages += [parsed_required[i] for i in range(1, len(parsed_required), 2)]

    var = {'homebrew_packages': []}
    for package in set(packages).difference(set(excepted_packages)):
        var['homebrew_packages'].append({'name': package})

    print(yaml.dump(var))


@cli.command()
def cask():
    cmd = 'ls /Applications'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    apps = p.communicate()[0].rstrip().split('\n')

    var = {'homebrew_cask_packages': []}
    for app in apps:
        app = app.replace('.app', '')
        cmd = 'brew cask search "%s"' % app
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = p.communicate()[0].rstrip().split('\n')

        if '==> Exact match' not in res:
            continue

        var['homebrew_cask_packages'].append({'name': res[res.index('==> Exact match') + 1]})

    print(yaml.dump(var))
