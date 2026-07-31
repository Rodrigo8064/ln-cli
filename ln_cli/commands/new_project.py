import subprocess
from pathlib import Path
from typing import Annotated

from rich.console import Console
from typer import Argument, Option, Typer

from ln_cli.commands import install_packages, install_packages_dev, packages

app = Typer()

console = Console()

FASTAPI_APP_TEMPLATE = """from fastapi import FastAPI, status

app = FastAPI()

@app.get('/health_check', status_code=status.HTTP_200_OK)
def health_check():
    return {'status': 'ok'}
"""


def create_fastapi_app_file(name: str) -> None:
    """
    Cria um app.py básico dentro da pasta do projeto.
    Parameters:
        name: Nome da pasta onde o arquivo deve ser criado

    Returns:
        A função adiciona o arquivo e retorna None

    Examples:
        create_fastapi_app_file('novo_projeto')
    """
    app_file = Path(name) / 'app.py'
    app_file.write_text(FASTAPI_APP_TEMPLATE)


@app.command()
def api(
    name: Annotated[str, Argument(..., help='Cria um projeto')],
    fastapi: Annotated[
        bool,
        Option('--fastapi', help='Instala dependências do FastAPI'),
    ] = False,
    django: Annotated[
        bool, Option('--django', help='Instala dependências do Django')
    ] = False,
    dev: Annotated[
        bool,
        Option('--dev', help='Instala dependências de desenvolvimento'),
    ] = False,
):
    if fastapi and django:
        console.print('Escolha somente uma flag: --fastapi ou --django')
        return

    subprocess.run(['poetry', 'new', '--flat', name], check=True)

    console.print('[green]Projeto criado[/]')

    if fastapi:
        install_packages(packages['fastapi'], name)
        create_fastapi_app_file(name)
        console.print('[green]app.py criado![/]')
    if django:
        install_packages(packages['django'], name)
    if dev:
        install_packages_dev(packages['dev'], name)
