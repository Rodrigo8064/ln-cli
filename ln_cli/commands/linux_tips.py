from typing import Annotated

from rich.console import Console
from rich.table import Table
from typer import Argument, Typer

from ln_cli.commands import COMMANDS_TYPES

app = Typer()

console = Console()


def tips_for_commands_type(command_type: str) -> dict:
    """
    Retorna uma Dicionário com comandos para usar no shell e sua descrição

    Parameters:
        command_type: Tipo de comando a ser retornado

    Returns:
        Um dicionário com o tipo e seus comandos.

    Raises:
        KeyError: Quando é passado um tipo que não está listado.

    Examples:
        tips_for_commands_type('texto')
        {'grep': 'pesquisa por termos dentro de arquivos',
        'sed': 'edita texto em fluxo (substituições, remoções, ...)',
        'awk': 'processa e manipula texto em colunas/campos',
        'cut': 'extrai colunas ou campos de uma linha',
        'sort': 'ordena linhas de um arquivo',
        'uniq': 'remove ou conta linhas duplicadas',
        'wc': 'conta linhas, palavras e caracteres',
        'tr': 'traduz ou remove caracteres',
        'cat': 'mostra o conteúdo completo de um arquivo',
        'head': 'mostra as primeiras linhas de um arquivo',
        'tail': 'mostra as últimas linhas',
        'less': 'visualiza arquivos grandes com paginação'}
    """
    command_type = command_type.lower()
    try:
        commands_list = COMMANDS_TYPES[command_type]
    except KeyError:
        raise KeyError(
            'Esse tipo de comando não existe, '
            f'tente os comando desta lista {list(COMMANDS_TYPES.keys())}'
        )
    return commands_list


@app.command()
def commands(
    command_type: Annotated[
        str,
        Argument(help='Escolha um dos tipos listado (texto, arquivos, ...)'),
    ],
):
    """
    Lista comandos que podem ser utilzidos no terminal.

    Tipos de comando:

    texto: Processamento de texto,
    arquivos: Visualização de arquivos,
    diretorios: Arquivos e diretórios,
    permissoes: Permissões e propriedades,
    processos: Processos e desempenho,
    rede: Rede,
    compactar: Compactação e arquivamento,
    sistema: Usuário e sistema,
    redirecionamento: Redirecionamento e pipes
    """
    table = Table()
    table.add_column('Nome')
    table.add_column('Descrição')

    results = tips_for_commands_type(command_type).items()
    for result in results:
        table.add_row(*result, end_section=True)

    console.print(table)
