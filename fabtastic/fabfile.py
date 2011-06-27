from fabric.api import *
from fabric.contrib.files import *
from fabric.contrib import django
from fabtastic import *
from time import sleep


# sets up some envs
fabtastic.init()


def local():
    """Use localhost as target"""

    env.directory = '/home/user/myproject'
    env.hosts = ['localhost']
    env.confdir = '%s/conf/local' % env.directory # keep local settings on git
    # sys_admin = local_user by default

def stage():
    env.directory = '/opt/system_user/projectname' # I setup a system user with home i.e /opt/my_client
    env.hosts = ['my_staging_server']
    env.confdir = '%s/conf/staging' % env.directory # staging settings also on git
    # sys_admin = local_user by default


def prod():
    env.directory = '/opt/system_user/projectname'
    env.hosts = [] # if you have several i specify on command line
    env.confdir = '/etc/projectname' # mega secret config files
    env.sys_admin = 'superuser' # a user with mega sudo rights


# TODO: full example of a deployment

def deploy():
    SetupNginx()

def redeploy():
    pass

def update():
    pass

def reset():
    pass
