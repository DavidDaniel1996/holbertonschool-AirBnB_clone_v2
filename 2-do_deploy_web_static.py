#!/usr/bin/python3
""" Generates .tgz archive from web_static """

from genericpath import exists
from posixpath import split
from fabric.api import hosts, env
from fabric.operations import local, run, put
from datetime import datetime
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
def do_deploy(archive_path):
    """ Deploys archive """
    if exists(archive_path) is False:
        return False
    file_name = archive_path.split('/')[1]
    dir_name = file_name.split('.')[0]

    put(archive_path, '/tmp/')
    run('mkdir -p /data/web_static/releases/{}'.format(dir_name))
    run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
        .format(file_name, dir_name))
    run('rm /tmp/{}'.format(file_name))
    run('rm -rf /data/web_static/current')
    run('ln -sf /data/web_static/releases/{}/ /data/web_static/current'
        .format(dir_name))

    return True
