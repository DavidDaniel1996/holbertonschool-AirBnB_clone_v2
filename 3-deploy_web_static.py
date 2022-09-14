#!/usr/bin/python3
"""fabfile to compress directory"""

from fabric.api import env, local, run, cd, put, runs_once
from datetime import datetime
import os

env.abort_exception = Exception
env.user = 'ubuntu'
env.hosts = ['184.73.131.136', '3.93.174.162']


@runs_once
def do_pack():
    """ Pack directory into .tgz file with specified format """

    try:
        t = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        name = "versions/web_static_{}.tgz".format(t)
        local("mkdir -p versions")
        res = local("tar -cvzf {} web_static".format(name))
        return(name)
    except Exception:
        return None


def do_deploy(archive_path=''):
    """ Distributes archive to remote servers """

    if os.path.exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.rsplit('/', 1)[1]
        put(archive_path, remote_path="/tmp/{}".format(file_name))

        file_pre = file_name[:-4]
        with cd('/tmp/'):
            run('mkdir -p /data/web_static/releases/{}'.format(file_pre))
            run('tar -zxf {} --directory /data/web_static/releases/{}'
                .format(file_name, file_pre))
            run(('mv /data/web_static/releases/{}/web_static/* '
                '/data/web_static/releases/{}/').format(file_pre, file_pre))
            run('rm -rf /data/web_static/releases/{}/web_static'
                .format(file_pre))
            run('rm -f {}'.format(file_name))
            run('rm -f /data/web_static/current')
            run('ln -sf /data/web_static/releases/{}/ /data/web_static/current'
                .format(file_pre))
            return True
    except Exception:
        return False


def deploy():
    """ Packs and deploys web servers defined above """

    archive = do_pack()
    if archive is False:
        return False
    result = do_deploy(archive_path=archive)
    return result
