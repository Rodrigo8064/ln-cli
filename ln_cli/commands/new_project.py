import subprocess
from typing import Annotated

from rich.console import Console
from typer import Argument, Option, Typer

from ln_cli.commands import install_packages, install_packages_dev, packages

app = Typer()

console = Console()


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
    if django:
        install_packages(packages['django'], name)
    if dev:
        install_packages_dev(packages['dev'], name)
