
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

    def restart(self):
        raise NotImplementedError

    def setup(self):
        self.install()
        self.configure()
        self.restart()


# TODO: For now everything is on one file, but I'll split things up once this grows to long

class fabNginx(FabricCommand):

    def install(self):
        install_packages('nginx')

    def configure(self):
        with settings(user=env.sys_admin):
            sudo('ln -sf %s/nginx/nginx.conf /etc/nginx/sites-enabled/%s' % (env.conf_dir, env.projectname))

    def restart(self):
        with settings(user=env.sys_admin):
            sudo('/etc/init.d/nginx restart')

class fabPostgresql(FabricCommand):
    """Install Postgres 8.4"""

    def install(self):
        install_packages('postgresql-8.4')

    def configure(self):
        with settings(user=env.sys_admin):
            sudo('psql < %s/postgresql/postgres.sql' % env.conf_dir, user='postgres')

    def restart(self):
        pass 

class fabSSH():
    # TODO: configuring users
    pass

def fabCompass():
    pass


class fabDjangoGunicorn(FabricCommand):

    def install(self):
        # latest ubuntu supervisor doesnt work, we install with pip for now
        #install_package('supervisor')
        with settings(user=env.sys_admin):
            pass

    def configure(self):
        with settings(user=env.sys_admin):
            sudo('ln -sf %s/gunicorn/supervisord.conf /etc/supervisor/conf.d/%s.conf' % (env.conf_dir,env.projectname))

    def restart(self):
        with settings(user=env.sys_admin):
            sudo('supervisorctl reload')
            sleep(5)
            sudo('supervisorctl restart %s' % env.projectname)


class fabCelery():
    def setup(self):
        with settings(user=env.sys_admin):
            sudo('ln -sf %s/rh2/conf/celery/supervisor.conf /etc/supervisor/conf.d/celery.conf' % env.directory)
            sudo('supervisorctl reload')
            sleep(5)
            sudo('supervisorctl restart celery')


class fabLocalSettings():

    def setup(self):
        with cd(env.directory):
            run('ln -sf %s/django/settings.py %s/local_settings.py' % (env.conf_dir, env.projectname))

