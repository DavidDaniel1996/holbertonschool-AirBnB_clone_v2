#!/usr/bin/python3
""" Generates .tgz archive from web_static """

from genericpath import exists
from fabric.operations import local
from datetime import datetime
import os
import tarfile


def do_pack():
    if (exists('versions') is False):
        local('sudo mkdir versions')

    local('sudo chown -R david:david versions')
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    name = f"web_static_{now}.tgz"

    with tarfile.open(f'versions/{name}', 'w:gz') as tarhandle:
        for root, dirs, files in os.walk('web_static'):
            for f in files:
                tarhandle.add(os.path.join(root, f))

    if (exists(f'versions/{name}') is True):
        return (f'versions/{name}')
    else:
        return (None)
