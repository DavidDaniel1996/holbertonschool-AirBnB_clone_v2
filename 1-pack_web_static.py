#!/usr/bin/python3
""" Generates .tgz archive from web_static """

from genericpath import exists
from fabric.api import env
from fabric.operations import local
from datetime import datetime
import os

env.hosts = ['127.0.0.1']


def do_pack():
    if (exists('versions') is False):
        os.mkdir('versions')
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    name = f"web_static_{now}.tgz"
    local(f'tar -cvzf versions/{name} web_static')
