import subprocess
from unittest.mock import patch

from ln_cli.commands.new_project import app


class TestApiCommand:
    @patch('ln_cli.commands.new_project.subprocess.run')
    def test_creat_project_without_flags(self, mock_run, runner):
        mock_run.return_value.returncode = 0
        result = runner.invoke(app, ['new_project'])
        mock_run.assert_called_once_with(
            ['poetry', 'new', '--flat', 'new_project'], check=True
        )
        assert result.exit_code == 0
        assert 'Projeto criado' in result.stdout

    @patch('ln_cli.commands.new_project.install_packages')
    @patch('ln_cli.commands.new_project.subprocess.run')
    def test_flag_fastapi_create_new_project_with_fastapi(
        self, mock_run, mock_install, runner
    ):
        result = runner.invoke(app, ['new_project', '--fastapi'])
        assert result.exit_code == 0
        mock_install.assert_called_once_with(
            [
                'fastapi[standard]',
                'sqlalchemy',
                'alembic',
                'psycopg[binary]',
            ],
            'new_project',
        )

    @patch('ln_cli.commands.new_project.install_packages')
    @patch('ln_cli.commands.new_project.subprocess.run')
    def test_flag_django_create_new_projetc_with_django_ninja(
        self, mock_run, mock_install, runner
    ):
        mock_run.return_value.returncode = 0

        result = runner.invoke(app, ['new_project', '--django'])

        assert result.exit_code == 0
        mock_install.assert_called_once_with(
            ['django-ninja', 'psycopg[binary]'], 'new_project'
        )

    @patch('ln_cli.commands.new_project.install_packages_dev')
    @patch('ln_cli.commands.new_project.subprocess.run')
    def test_flag_dev_install_dev_packages(
        self, mock_run, mock_install_dev, runner
    ):
        mock_run.return_value.returncode = 0

        result = runner.invoke(app, ['new_project', '--dev'])

        assert result.exit_code == 0
        mock_install_dev.assert_called_once_with(
            [
                'pytest',
                'taskipy',
                'ruff',
                'testcontainers',
                'pytest-cov',
            ],
            'new_project',
        )

    @patch('ln_cli.commands.new_project.install_packages')
    @patch('ln_cli.commands.new_project.install_packages_dev')
    @patch('ln_cli.commands.new_project.subprocess.run')
    def test_flag_fastapi_and_dev_install_packages(
        self, mock_run, mock_install_dev, mock_install, runner
    ):
        mock_run.return_value.returncode = 0

        result = runner.invoke(app, ['new_project', '--fastapi', '--dev'])

        assert result.exit_code == 0
        mock_install.assert_called_once()
        mock_install_dev.assert_called_once()

    @patch('ln_cli.commands.new_project.subprocess.run')
    def test_fastapi_and_django_return_error(self, mock_run, runner):
        result = runner.invoke(app, ['new_project', '--fastapi', '--django'])

        assert result.exit_code == 0
        assert 'Escolha somente uma flag' in result.stdout
        mock_run.assert_not_called()

    @patch('ln_cli.commands.new_project.subprocess.run')
    def test_falha_no_poetry_new_propaga_excecao(self, mock_run, runner):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'poetry')

        result = runner.invoke(app, ['new_project'])

        assert result.exit_code != 0
        assert isinstance(result.exception, subprocess.CalledProcessError)
