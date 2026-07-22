import shutil
import subprocess

from rich.console import Console
from typer import Exit, Typer, confirm, prompt

from ln_cli.commands import get_package_manager

app = Typer()
console = Console()


class InstallError(Exception):
    """Erro ao instalar um pacote via subprocess."""


def _require_package_manager() -> str:
    package_manager = get_package_manager()
    if package_manager is None:
        console.print(
            '[red]Nenhum gerenciador de pacotes suportado foi encontrado.[/]'
        )
        raise Exit(code=1)
    return package_manager


def install_pipx(package_manager: str) -> None:
    try:
        if package_manager == 'apt' or 'dnf':
            subprocess.run(
                ['sudo', package_manager, 'install', 'pipx'], check=True
            )
        else:
            subprocess.run(
                ['python3', '-m', 'pip', 'install', '--user', 'pipx'],
                check=True,
            )
        subprocess.run(['pipx', 'ensurepath'], check=True)
    except subprocess.CalledProcessError as error:
        raise InstallError(
            f'Falha ao instalar o pipx (código de saída {error.returncode}).'
        ) from error
    except FileNotFoundError as error:
        raise InstallError(
            f'Comando não encontrado: {error.filename}'
        ) from error


@app.command()
def pipx():
    """Instalar pipx via gerenciador de pacotes ou pip."""
    package_manager = _require_package_manager()
    if shutil.which('pipx'):
        console.print('[green]Pipx já esta instalado[/green]')
        raise Exit(code=0)

    confirm('Deseja instalar o pipx?', abort=True)
    install_pipx(package_manager)
    console.print('[green]Pipx instalado com sucesso[/green]')


@app.command()
def poetry():
    """Instalar poetry via pipx ou instalador oficial."""
    package_manager = _require_package_manager()
    metodo = prompt(
        'Como deseja instalar o poetry?\n'
        '  [1] Via pipx\n'
        '  [2] Via instalador oficial',
        type=int,
    )
    try:
        if metodo == 1:
            if not shutil.which('pipx'):
                console.print('[red]Pipx não foi encontrado[/red]')
                confirm('Deseja instalar o pipx?', abort=True)
                install_pipx(package_manager)
                console.print('[green]Pipx instalado com sucesso[/green]')
            subprocess.run(['pipx', 'install', 'poetry'], check=True)
            subprocess.run(
                ['pipx', 'inject', 'poetry', 'poetry-plugin-shell'], check=True
            )
        elif metodo == 2:
            result = subprocess.run(
                [
                    'curl',
                    '-sSL',
                    'https://install.python-poetry.org',
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                ['python3', '-'], input=result.stdout, check=True, text=True
            )
            subprocess.run(['poetry', 'self', 'add', 'poetry-plugin-shell'])
        else:
            console.print('[red]Opção inválida.')
            raise Exit(code=1)
    except InstallError as error:
        console.print(f'[red]{error}[/red]')
        raise Exit(code=1) from error
    except subprocess.CalledProcessError as error:
        console.print(
            f'[red]Falha ao instalar o poetry (código {error.returncode}).[/red]'
        )
        raise Exit(code=1) from error

    console.print('[green]Poetry instalado com sucesso[/green]')
