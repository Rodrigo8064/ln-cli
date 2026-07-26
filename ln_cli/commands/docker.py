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
):
    postgres_version = f'postgres:{tag}'
    subprocess.run(
        [
            'docker',
            'run',
            '-d',
            '--name',
            'app_database',
            '-e',
            'POSTGRES_USER=app_user',
            '-e',
            'POSTGRES_DB=app_db',
            '-e',
            'POSTGRES_PASSWORD=app_password',
            '-v',
            'pgdata:/var/lib/postgresql/',
            '-p',
            '5432:5432',
            postgres_version,
        ],
        check=True,
    )

    console.print('[green]DB Criado![/]')
