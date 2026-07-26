from unittest.mock import patch

from ln_cli.cli import app


class TestMainCallback:
    def test_without_subcommand(self, runner):
        result = runner.invoke(app, [])
        assert result.exit_code == 0
        assert 'Como utilizar' in result.stdout

    @patch('ln_cli.cli.__version__', '1.2.3')
    def test_flag_version_show_version(self, runner):
        result = runner.invoke(app, ['--version'])
        assert result.exit_code == 0
        assert '1.2.3' in result.stdout

    def test_subcommands_registered(self, runner):
        result = runner.invoke(app, ['--help'])
        assert result.exit_code == 0
        assert 'new' in result.stdout
        assert 'install' in result.stdout
        assert 'docker' in result.stdout
