import subprocess
from typing import Annotated

from rich.console import Console
from typer import Argument, Typer

app = Typer()

console = Console()


@app.command()
def postgres(
    tag: Annotated[
        str, Argument(help='Passa uma TAG para o postgres')
    ] = 'latest',
    name: Annotated[
        str, Argument(help='Nome para o conteiner')
    ] = 'app_database',
    user: Annotated[str, Argument(help='Usuario do banco de dados')] = 'user',
    db: Annotated[
        str, Argument(help='Nome do banco de dados')
    ] = 'postgres_db',
    port: Annotated[
        str, Argument(help='Porta espelho do banco de dados')
    ] = '5432',
):
    """
    Sobe um conteiner com a imagem postgres para testes em api

    Args:
        tag: Passa uma TAG para o postgres, latest é utilizado por default.
        name: Passa um nome para o conteiner, app_database por default.
        user: Passa um nome de usuario para o banco de dados, user por default.
        db: Indica qual o nome do banco de dados, postgres_db por default.

    Examples:
        ```bash
        lunar docker postgres 17
        ```
    """
    postgres_version = f'postgres:{tag}'
    subprocess.run(
        [
            'docker',
            'run',
            '-d',
            '--name',
            name,
            '-e',
            f'POSTGRES_USER={user}',
            '-e',
            f'POSTGRES_DB={db}',
            '-e',
            'POSTGRES_PASSWORD=password',
            '-v',
            'pgdata:/var/lib/postgresql/',
            '-p',
            f'5432:{port}',
            postgres_version,
        ],
        check=True,
    )

    console.print('[green]DB Criado![/]')
