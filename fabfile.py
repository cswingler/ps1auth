from fabric.api import *
from cuisine import *


env.use_ssh_config = True

def staging():
    env.root = '/srv/http/arbitrarion.com/app/'
    env.hosts = ['ps1auth-staging']
    env.mode = 'staging'
    env.restart = lambda : run('killall /srv/http/arbitrarion.com/venv/bin/python3', warn_only=True)

def production():
    env.root = '/srv/http/members.pumpingstationone.org/app'
    env.hosts = ['ps1auth-production']
    env.mode = 'production'
    env.restart = lambda : run('killall /srv/http/members.pumpingstationone.org/venv/bin/python3', warn_only=True)

def deploy():
    with cd('%(root)s' % env):
        run('git pull')
        with prefix('source ~/config.sh'):
            run('../venv/bin/pip install -r requirements/%(mode)s.txt' % env)
            run('../venv/bin/python ./manage.py syncdb --noinput')
            run('../venv/bin/python ./manage.py migrate --noinput')
            run('../venv/bin/python ./manage.py collectstatic --noinput')
            env.restart()

