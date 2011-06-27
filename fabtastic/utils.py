from fabric.api import *
from fabric.contrib.files import *
#from fabric.contrib import django
import os
from time import sleep
import fabric.state

env = fabric.state.env


def init():
    """
    Sets up some default variables
    """
    env.local_dir    = os.path.abspath(os.path.dirname(__file__))
    env.project_name = env.LOCAL_DIR.split('/')[-1].lower()
    env.virtualenv   = env.project_name
    env.sys_admin    = env.local_user

    
def help():    # TODO: dev/dep
    print """
          TODO: will automatically print a help using __doc__ and targets
          """

# --- Virtualenv  & PIP ---

def ve(virtualenv):
    """Set virtualenv"""
    env.virtualenv = virtualenv

def ve_run(cmd):
    with cd(env.directory):
        run("""
               export WORKON_HOME=%s &&
               source /usr/local/bin/virtualenvwrapper.sh &&
               workon %s &&
               %s
               """ % (env.workon_home, env.virtualenv, cmd)
        )

def create_virtualenv():
    # Create virtualenv, specify name with ve option

    run("""
           export WORKON_HOME=%s &&
           source /usr/local/bin/virtualenvwrapper.sh &&
           mkvirtualenv --no-site-packages %s
        """ % (env.workon_home, env.virtualenv))


def pip_sys_install(package):
    """Installs using the system PIP (not in a ve)"""
    sudo('pip install %s' % package)

def pip_install_requirements():
    with cd(env.directory):
        ve_run("""export PIP_REQUIRE_VIRTUALENV=true &&
              export PIP_RESPECT_VIRTUALENV=true &&
              export PIP_USE_MIRRORS=true &&

              yes w | pip install -q -r requirements.pip
              """
        )

def pip_install_stable():
    with cd(env.directory):
        ve_run("""export PIP_REQUIRE_VIRTUALENV=true &&
              export PIP_RESPECT_VIRTUALENV=true &&
              export PIP_USE_MIRRORS=true &&

              yes w | pip install -q -r stable.pip
              """
        )


def pip_install_project():
    """Install project in Virtualenv"""
    with cd(env.directory):
        ve_run('pip install -e ./')



# --- APT Install system packages

def install_packages(packages):
    """
    Install system packages via aptitude
    """

    if isinstance(packages,str):
        package_string = packages
    else:
        package_string = " ".join(packages)

    with settings(user=env.sys_admin, use_shell=False):
        sudo("aptitude install -y -q %s" % package_string)


def build_dep(packages):
    """
    Run aptitude build dependencies
    """
    if isinstance(packages, str):
        package_string = packages
    else:
        package_string = " ".join(packages)

    with settings(user=env.sys_admin, use_shell=False):
        sudo("aptitude build_dep -y -q %s" % package_string)

