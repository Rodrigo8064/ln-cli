import re

from pytest import raises

from ln_cli.commands import COMMANDS_TYPES
from ln_cli.commands.linux_tips import app, tips_for_commands_type


def test_tips_for_commands_type_return_data():
    command_type = 'texto'

    result = tips_for_commands_type(command_type)

    assert 'grep' in result.keys()


def test_tips_for_commands_type_return_error():
    command_type = 'cangurus'

    mensagem_de_erro = (
        'Esse tipo de comando não existe, '
        f'tente os comando desta lista {list(COMMANDS_TYPES.keys())}'
    )

    with raises(KeyError, match=re.escape(mensagem_de_erro)):
        tips_for_commands_type(command_type)


class TestCommands:
    def test_commands_return_tips_for_text(self, runner):
        result = runner.invoke(app, ['texto'])
        assert result.exit_code == 0
        assert 'grep' in result.stdout

    def test_commands_accepts_uppercase_letters(self, runner):
        result = runner.invoke(app, ['TEXTO'])
        assert result.exit_code == 0
        assert 'grep' in result.stdout

    def test_commands_invalid_type_returns_key_error(self, runner):
        result = runner.invoke(app, ['cangurus'])
        assert result.exit_code != 0
        assert isinstance(result.exception, KeyError)
