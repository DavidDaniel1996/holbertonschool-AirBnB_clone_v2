#!/usr/bin/python3
""" Generates .tgz archive from web_static """

from genericpath import exists
from fabric.api import hosts, env
from fabric.operations import local, run, put
from datetime import datetime
from contextlib import contextmanager
import os


def do_pack():
    """ Creates archive """
    env.hosts = ['127.0.0.1']
    if (exists('versions') is False):
        os.mkdir('versions')
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    name = "web_static_{}.tgz".format(now)
    local('tar -cvzf versions/{} web_static'.format(name))


@hosts(['54.89.173.194', '52.91.171.59'])
@contextmanager
def do_deploy(archive_path):
    """ Deploys archive """

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
