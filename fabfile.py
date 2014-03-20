from __future__ import with_statement
import os

from fabric.api import abort, run, sudo, env, cd, local


def staging():
    env.hosts = ['<user@site.com>']
    env.directory = '</path/to/project/>'
    env.activate = 'source ' + os.path.join(env.directory, '.env/bin/activate')

def virtualenv(command):
    with cd(env.directory):
        run(env.activate + '&&' + command)

def deploy():
    virtualenv('git checkout master')
    virtualenv('git pull origin master')
    virtualenv('make syncdb')
    virtualenv('make manage CMD="collectstatic --noinput"')
    virtualenv('pip install -r %srequirements.txt' % env.directory)
    virtualenv('make uwsgi_reload')
