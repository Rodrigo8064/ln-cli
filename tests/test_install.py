import subprocess
from unittest.mock import patch

from ln_cli.commands.install import app


class TestPipxCommand:
    @patch(
        'ln_cli.commands.install.shutil.which', return_value='/usr/bin/pipx'
    )
    def test_already_install_do_nothing(self, mock_which, runner):
        result = runner.invoke(app, ['pipx'])
        assert result.exit_code == 0
        assert 'já esta instalado' in result.stdout

    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value=None)
    def test_without_package_manager(self, mock_gpm, mock_which, runner):
        result = runner.invoke(app, ['pipx'])
        assert result.exit_code == 1
        assert 'Nenhum gerenciador de pacotes suportado' in result.stdout

    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value='apt')
    def test_user_abort_installation(self, mock_gpm, mock_which, runner):
        result = runner.invoke(app, ['pipx'], input='n\n')
        assert result.exit_code != 0

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value='apt')
    def test_confirm_installation_with_apt(
        self, mock_gpm, mock_which, mock_run, runner
    ):
        result = runner.invoke(app, ['pipx'], input='y\n')
        assert result.exit_code == 0
        called_commands = [c.args[0] for c in mock_run.call_args_list]
        assert ['sudo', 'apt', 'install', 'pipx'] in called_commands
        assert ['pipx', 'ensurepath'] in called_commands
        assert 'Pipx instalado com sucesso' in result.stdout

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value='dnf')
    def test_confirm_installation_with_dnf(
        self, mock_gpm, mock_which, mock_run, runner
    ):
        result = runner.invoke(app, ['pipx'], input='y\n')
        assert result.exit_code == 0
        called_commands = [c.args[0] for c in mock_run.call_args_list]
        assert ['sudo', 'dnf', 'install', 'pipx'] in called_commands
        assert ['pipx', 'ensurepath'] in called_commands
        assert 'Pipx instalado com sucesso' in result.stdout

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch(
        'ln_cli.commands.install.get_package_manager', return_value='pacman'
    )
    def test_confirm_installation_with_pip_and_pacman(
        self, mock_gpm, mock_which, mock_run, runner
    ):
        result = runner.invoke(app, ['pipx'], input='y\n')
        assert result.exit_code == 0
        called_commands = [c.args[0] for c in mock_run.call_args_list]
        assert [
            'python3',
            '-m',
            'pip',
            'install',
            '--user',
            'pipx',
        ] in called_commands
        assert ['sudo', 'pacman', '-S', 'pipx'] not in called_commands

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value='apt')
    def test_fail_run_ensurepath_report_error(
        self, mock_gpm, mock_which, mock_run, runner
    ):
        def side_effect(command, **kwargs):
            if command[:2] == ['pipx', 'ensurepath']:
                raise subprocess.CalledProcessError(1, command)
            return None

        mock_run.side_effect = side_effect
        result = runner.invoke(app, ['pipx'], input='y\n')
        assert result.exit_code == 1
        assert 'Falha ao instalar o pipx' in result.stdout


class TestPoetryCommand:
    @patch(
        'ln_cli.commands.install.shutil.which', return_value='/usr/bin/poetry'
    )
    def test_already_install_do_nothing(self, mock_which, runner):
        result = runner.invoke(app, ['poetry'])
        assert result.exit_code == 0
        assert 'já está instalado' in result.stdout

    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value=None)
    def test_without_suport_package_manager(
        self, mock_gpm, mock_which, runner
    ):
        result = runner.invoke(app, ['poetry'], input='1\n')
        assert result.exit_code == 1

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which')
    @patch('ln_cli.commands.install.get_package_manager', return_value='apt')
    def test_with_pipx(self, mock_gpm, mock_which, mock_run, runner):
        # poetry não está instalado, mas o pipx sim.
        mock_which.side_effect = lambda cmd: (
            None if cmd == 'poetry' else '/usr/bin/pipx'
        )
        result = runner.invoke(app, ['poetry'], input='1\n')
        assert result.exit_code == 0
        called_commands = [c.args[0] for c in mock_run.call_args_list]
        assert ['pipx', 'install', 'poetry'] in called_commands
        assert [
            'pipx',
            'inject',
            'poetry',
            'poetry-plugin-shell',
        ] in called_commands
        assert 'Poetry instalado com sucesso' in result.stdout

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value='apt')
    def test_with_pipx_install_pipx_first(
        self, mock_gpm, mock_which, mock_run, runner
    ):
        result = runner.invoke(app, ['poetry'], input='1\ny\n')
        assert result.exit_code == 0
        assert 'Pipx instalado com sucesso' in result.stdout
        assert 'Poetry instalado com sucesso' in result.stdout

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value='apt')
    def test_with_official_installer(
        self, mock_gpm, mock_which, mock_run, runner
    ):
        mock_run.return_value.stdout = 'echo instalando'
        result = runner.invoke(app, ['poetry'], input='2\n')
        assert result.exit_code == 0
        called_commands = [c.args[0] for c in mock_run.call_args_list]
        assert any(cmd[:2] == ['curl', '-sSL'] for cmd in called_commands)
        assert ['python3', '-'] in called_commands
        assert [
            'poetry',
            'self',
            'add',
            'poetry-plugin-shell',
        ] in called_commands

    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value='apt')
    def test_invalid_option(self, mock_gpm, mock_which, runner):
        result = runner.invoke(app, ['poetry'], input='9\n')
        assert result.exit_code == 1
        assert 'Opção inválida' in result.stdout


class TestLazygitCommand:
    @patch(
        'ln_cli.commands.install.shutil.which', return_value='/usr/bin/lazygit'
    )
    def test_already_install_do_nothing(self, mock_which, runner):
        result = runner.invoke(app, ['lazygit'])
        assert result.exit_code == 0
        assert 'já está instalado' in result.stdout

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value='dnf')
    def test_install_with_dnf(self, mock_gpm, mock_which, mock_run, runner):
        result = runner.invoke(app, ['lazygit'])
        assert result.exit_code == 0
        called_commands = [c.args[0] for c in mock_run.call_args_list]
        assert [
            'sudo',
            'dnf',
            'copr',
            'enable',
            'dejan/lazygit',
        ] in called_commands
        assert ['sudo', 'dnf', 'install', 'lazygit'] in called_commands

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value='apt')
    def test_with_apt(self, mock_gpm, mock_which, mock_run, runner):
        result = runner.invoke(app, ['lazygit'])
        assert result.exit_code == 0
        called_commands = [c.args[0] for c in mock_run.call_args_list]
        assert all('copr' not in cmd for cmd in called_commands)

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value='apt')
    def test_fail_install_report_error(
        self, mock_gpm, mock_which, mock_run, runner
    ):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'apt')
        result = runner.invoke(app, ['lazygit'])
        assert result.exit_code == 1
        assert 'Falha ao instalar lazygit' in result.stdout


class TestLazydockerCommand:
    @patch(
        'ln_cli.commands.install.shutil.which',
        return_value='/usr/bin/lazydocker',
    )
    def test_already_install_do_nothing(self, mock_which, runner):
        result = runner.invoke(app, ['lazydocker'])
        assert result.exit_code == 0
        assert 'já está instalado' in result.stdout

    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    def test_without_curl_report_error(self, mock_which, runner):
        result = runner.invoke(app, ['lazydocker'])
        assert result.exit_code == 1
        assert 'curl não foi encontrado' in result.stdout

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which')
    def test_install_with_script_curl_and_bash(
        self, mock_which, mock_run, runner
    ):
        # lazydocker não está instalado, mas o curl sim.
        mock_which.side_effect = lambda cmd: (
            '/usr/bin/curl' if cmd == 'curl' else None
        )
        mock_run.return_value.stdout = 'echo instalando lazydocker'
        result = runner.invoke(app, ['lazydocker'])
        assert result.exit_code == 0
        called_commands = [c.args[0] for c in mock_run.call_args_list]
        assert any(cmd[0] == 'curl' for cmd in called_commands)
        assert ['bash'] in called_commands
        assert 'lazydocker instalado com sucesso' in result.stdout

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which')
    def test_fail_download_report_error(self, mock_which, mock_run, runner):
        mock_which.side_effect = lambda cmd: (
            '/usr/bin/curl' if cmd == 'curl' else None
        )
        mock_run.side_effect = subprocess.CalledProcessError(1, 'curl')
        result = runner.invoke(app, ['lazydocker'])
        assert result.exit_code == 1
        assert 'Falha ao instalar o lazydocker' in result.stdout


class TestRipgrepCommand:
    @patch('ln_cli.commands.install.shutil.which', return_value='/usr/bin/rg')
    def test_already_install_do_nothing(self, mock_which, runner):
        result = runner.invoke(app, ['ripgrep'])
        assert result.exit_code == 0
        assert 'já está instalado' in result.stdout

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch(
        'ln_cli.commands.install.get_package_manager', return_value='pacman'
    )
    def test_install_with_package_manager(
        self, mock_gpm, mock_which, mock_run, runner
    ):
        result = runner.invoke(app, ['ripgrep'])
        assert result.exit_code == 0
        mock_run.assert_called_once_with(
            ['sudo', 'pacman', '-S', 'ripgrep'], check=True
        )
        assert 'Ripgrep instalado com sucesso' in result.stdout

    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value=None)
    def test_without_suported_package_manager(
        self, mock_gpm, mock_which, runner
    ):
        result = runner.invoke(app, ['ripgrep'])
        assert result.exit_code == 1
        assert 'Nenhum gerenciador de pacotes suportado' in result.stdout

    @patch('ln_cli.commands.install.subprocess.run')
    @patch('ln_cli.commands.install.shutil.which', return_value=None)
    @patch('ln_cli.commands.install.get_package_manager', return_value='apt')
    def test_fail_installation_report_error(
        self, mock_gpm, mock_which, mock_run, runner
    ):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'apt')
        result = runner.invoke(app, ['ripgrep'])
        assert result.exit_code == 1
        assert 'Falha ao instalar ripgrep' in result.stdout
