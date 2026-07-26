import subprocess
from unittest.mock import patch

from ln_cli.commands.docker import app


class TestPostgresCommand:
    @patch('ln_cli.commands.docker.subprocess.run')
    def test_tag_latest_by_defout(self, mock_run, runner):
        result = runner.invoke(app, [])
        assert result.exit_code == 0
        args_chamados = mock_run.call_args[0][0]
        assert args_chamados[-1] == 'postgres:latest'

    @patch('ln_cli.commands.docker.subprocess.run')
    def test_with_tag(self, mock_run, runner):
        result = runner.invoke(app, ['16'])
        assert result.exit_code == 0
        args_chamados = mock_run.call_args[0][0]
        assert args_chamados[-1] == 'postgres:16'

    @patch('ln_cli.commands.docker.subprocess.run')
    def test_check_env(self, mock_run, runner):
        runner.invoke(app, [])
        args_chamados = mock_run.call_args[0][0]
        assert 'POSTGRES_USER=app_user' in args_chamados
        assert 'POSTGRES_DB=app_db' in args_chamados
        assert 'POSTGRES_PASSWORD=app_password' in args_chamados
        assert '5432:5432' in args_chamados
        assert mock_run.call_args.kwargs.get('check') is True

    @patch('ln_cli.commands.docker.subprocess.run')
    def test_falha_ao_iniciar_docker_propaga_excecao(self, mock_run, runner):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'docker')
        result = runner.invoke(app, [])
        assert result.exit_code != 0
        assert isinstance(result.exception, subprocess.CalledProcessError)
