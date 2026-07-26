import shutil
import subprocess

from rich.console import Console
from typer import Exit, Typer, confirm, prompt

from ln_cli.commands import INSTALL_COMMANDS, get_package_manager

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


def run_install(package_manager: str, package: str) -> None:
    """Instala `package` usando o `package_manager` informado."""
    try:
        command = INSTALL_COMMANDS[package_manager](package)
        subprocess.run(command, check=True)
    except KeyError as error:
        raise InstallError(
            f'Gerenciador de pacotes não suportado: {package_manager}'
        ) from error
    except subprocess.CalledProcessError as error:
        raise InstallError(
            f'Falha ao instalar {package} (código de saída {error.returncode}).'
        ) from error
    except FileNotFoundError as error:
        raise InstallError(
            f'Comando não encontrado: {error.filename}'
        ) from error


def install_pipx(package_manager: str) -> None:
    try:
        if package_manager in ('apt', 'dnf'):
            run_install(package_manager, 'pipx')
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


def install_curl(package_manager: str) -> None:
    if shutil.which('curl'):
        return
    run_install(package_manager, 'curl')


@app.command()
def pipx():
    """Instalar pipx via gerenciador de pacotes ou pip."""
    if shutil.which('pipx'):
        console.print('[green]Pipx já esta instalado[/green]')
        raise Exit(code=0)

    package_manager = _require_package_manager()
    confirm('Deseja instalar o pipx?', abort=True)
    try:
        install_pipx(package_manager)
    except InstallError as error:
        console.print(f'[red]{error}[/red]')
        raise Exit(code=1) from error
    console.print('[green]Pipx instalado com sucesso[/green]')


@app.command()
def poetry():
    """Instalar poetry via pipx ou instalador oficial."""
    if shutil.which('poetry'):
        console.print('Poetry já está instalado')
        raise Exit(code=0)
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
            install_curl(package_manager)
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
            subprocess.run(
                ['poetry', 'self', 'add', 'poetry-plugin-shell'], check=True
            )
        else:
            console.print('[red]Opção inválida.[/red]')
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


@app.command()
def lazygit():
    """Instalar lazygit via gerenciador de pacotes."""
    if shutil.which('lazygit'):
        console.print('lazygit já está instalado')
        raise Exit(code=0)

    package_manager = _require_package_manager()
    try:
        if package_manager == 'dnf':
            subprocess.run(
                ['sudo', 'dnf', 'copr', 'enable', 'dejan/lazygit'],
                check=True,
            )
        run_install(package_manager, 'lazygit')
    except InstallError as error:
        console.print(f'[red]{error}[/red]')
        raise Exit(code=1) from error
    except subprocess.CalledProcessError as error:
        console.print(
            f'[red]Falha ao instalar o lazygit (código {error.returncode}).[/red]'
        )
        raise Exit(code=1) from error

    console.print('[green]Lazygit instalado com sucesso[/green]')


@app.command()
def lazydocker():
    """Instalar binario do lazydocker via curl."""
    if shutil.which('lazydocker'):
        console.print('lazydocker já está instalado')
        raise Exit(code=0)

    if not shutil.which('curl'):
        console.print('[red]curl não foi encontrado[/red]')
        raise Exit(code=1)

    try:
        result = subprocess.run(
            [
                'curl',
                'https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh',
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(['bash'], input=result.stdout, check=True, text=True)
    except subprocess.CalledProcessError as error:
        console.print(
            f'[red]Falha ao instalar o lazydocker (código {error.returncode}).[/red]'
        )
        raise Exit(code=1) from error

    console.print('[green]lazydocker instalado com sucesso[/green]')


@app.command()
def ripgrep():
    """Instalar Ripgrep via gerenciador de pacotes."""
    if shutil.which('rg'):
        console.print('Ripgrep já está instalado')
        raise Exit(code=0)

    package_manager = _require_package_manager()
    try:
        run_install(package_manager, 'ripgrep')
    except InstallError as error:
        console.print(f'[red]{error}[/red]')
        raise Exit(code=1) from error
    except subprocess.CalledProcessError as error:
        console.print(
            f'[red]Falha ao instalar o ripgrep (código {error.returncode}).[/red]'
        )
        raise Exit(code=1) from error

    console.print('[green]Ripgrep instalado com sucesso[/green]')
