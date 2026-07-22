import shutil
import subprocess

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
