import shutil
import subprocess
from collections.abc import Callable

packages = {
    'fastapi': [
        'fastapi[standard]',
        'sqlalchemy',
        'alembic',
        'psycopg[binary]',
    ],
    'django': ['django-ninja', 'psycopg[binary]'],
    'dev': ['pytest', 'taskipy', 'ruff', 'testcontainers', 'pytest-cov'],
}


def install_packages(packages, name):
    subprocess.run(['poetry', 'add', *packages], cwd=name)


def install_packages_dev(packages, name):
    subprocess.run(['poetry', 'add', '--group', 'dev', *packages], cwd=name)


def get_package_manager() -> None | str:
    if shutil.which('apt'):
        return 'apt'
    if shutil.which('dnf'):
        return 'dnf'
    if shutil.which('pacman'):
        return 'pacman'
    return None


INSTALL_COMMANDS: dict[str, Callable[[str], list[str]]] = {
    'apt': lambda pkg: ['sudo', 'apt', 'install', pkg],
    'dnf': lambda pkg: ['sudo', 'dnf', 'install', pkg],
    'pacman': lambda pkg: ['sudo', 'pacman', '-S', pkg],
}
