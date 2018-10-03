from os import getcwd, path
from sys import path as sys_path


def fix():

    current_path = getcwd()
    parts = current_path.split('/')[:-1]
    new_path = '/{0}'.format(path.join(*parts))

    sys_path.append(new_path)
