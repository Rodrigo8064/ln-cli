import pytest
from typer.testing import CliRunner


@pytest.fixture
def runner():
    """CliRunner do Typer, usado para invocar os comandos da CLI nos testes"""
    return CliRunner()
