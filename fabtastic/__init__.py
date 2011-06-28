
#from fabric.api import *
import fabric.state
from utils import *

env = fabric.state.env




class FabricCommand(object):
    """
    Base class for class based Fabric (Fabtastic) commands
    """

    def __init__(self, **kwargs):
        self.setup()

    def configure(self):
        raise NotImplementedError

    def install(self):
        raise NotImplementedError

    def reload(self):
        raise NotImplementedError

    def setup(self):
        self.install()
        self.configure()
        self.reload()


# TODO: For now everything is on one file, but I'll split things up once this grows to long

class fabNginx(FabricCommand):

    def install(self):
        install_packages('nginx')

    def configure(self):
        with settings(user=env.sys_admin):
            sudo('ln -sf %s/nginx.conf /etc/nginx/sites-enabled/rh2' % env.confdir)

    def reload(self):
        with settings(user=env.sys_admin):
            sudo('/etc/init.d/nginx restart')

class fabPostgresql():
    """Install Postgres 8.4"""

    def install(self):
        install_packages('postgresql-8.4')

    def configure(self):
        with settings(user=env.sys_admin):
            sudo('psql < %s/postgresql/configure.sql' % env.confdir, user='postgres')


class fabSSH():
    # TODO: configuring users
    pass

def fabCompass():
    pass


class fabSupervisor():

    def install(self):
        # latest ubuntu supervisor doesnt work, we install with pip for now
        #install_package('supervisor')
        with settings(user=env.sys_admin):
            pass

    def configure(self):
        with settings(user=env.sys_admin):
            sudo('ln -sf %s/supervisord.conf /etc/supervisor/conf.d/rh2.conf' % env.conf)

    def restart(self):
        sudo('supervisorctl reload')
        sleep(5)
        sudo('supervisorctl restart celery')


def fabCelery():
    with settings(user=env.local_user):
        sudo('ln -sf %s/rh2/conf/celery/supervisor.conf /etc/supervisor/conf.d/celery.conf' % env.directory)
        sudo('supervisorctl reload')
        sleep(5)
        sudo('supervisorctl restart celery')


def fabLocalSettings():
    with cd(env.directory):
        run('ln -sf %s/settings.py %s/local_settings.py' % (env.conf ,env.project))

if __name__ == "__main__":

    # testing command
    # now testing Nginx
    init()
    env.hosts = ['localhost']
    fabNginx().setup()

