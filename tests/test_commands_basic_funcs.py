from unittest.mock import patch

from ln_cli.commands import (
    INSTALL_COMMANDS,
    get_package_manager,
    install_packages,
    install_packages_dev,
)


class TestInstallPackages:
    @patch('ln_cli.commands.subprocess.run')
    def test_install_packages_with_poetry_in_directory(self, mock_run):
        install_packages(
            [
                'fastapi',
                'sqlalchemy',
            ],
            'new_project',
        )
        mock_run.assert_called_once_with(
            ['poetry', 'add', 'fastapi', 'sqlalchemy'], cwd='new_project'
        )

    @patch('ln_cli.commands.subprocess.run')
    def test_install_packages_with_empty_list(self, mock_run):
        install_packages([], 'new_project')
        mock_run.assert_called_once_with(['poetry', 'add'], cwd='new_project')

    @patch('ln_cli.commands.subprocess.run')
    def test_install_packages_dev_with_poetry(self, mock_run):
        install_packages_dev(['pytest', 'ruff'], 'new_project')
        mock_run.assert_called_once_with(
            ['poetry', 'add', '--group', 'dev', 'pytest', 'ruff'],
            cwd='new_project',
        )


class TestGetPackageManager:
    @patch('ln_cli.commands.shutil.which')
    def test_return_apt(self, mock_which):
        mock_which.side_effect = lambda cmd: (
            '/user/bin/apt' if cmd == 'apt' else None
        )
        assert get_package_manager() == 'apt'

    @patch('ln_cli.commands.shutil.which')
    def test_return_dnf(self, mock_which):
        mock_which.side_effect = lambda cmd: (
            '/user/bin/dnf' if cmd == 'dnf' else None
        )
        assert get_package_manager() == 'dnf'

    @patch('ln_cli.commands.shutil.which')
    def test_return_pacman(self, mock_which):
        mock_which.side_effect = lambda cmd: (
            '/user/bin/pacman' if cmd == 'pacman' else None
        )
        assert get_package_manager() == 'pacman'

    @patch('ln_cli.commands.shutil.which', return_value=None)
    def test_return_none(self, mock_which):
        assert get_package_manager() is None


class TestInstallCommands:
    def test_command_apt(self):
        assert INSTALL_COMMANDS['apt']('curl') == [
            'sudo',
            'apt',
            'install',
            'curl',
        ]

    def test_command_dnf(self):
        assert INSTALL_COMMANDS['dnf']('curl') == [
            'sudo',
            'dnf',
            'install',
            'curl',
        ]

    def test_command_pacman(self):
        assert INSTALL_COMMANDS['pacman']('curl') == [
            'sudo',
            'pacman',
            '-S',
            'curl',
        ]
