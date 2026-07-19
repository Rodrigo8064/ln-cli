import subprocess

from typer import Argument, Typer, colors, secho

app = Typer()


@app.command()
def new(
    name: str = Argument(..., help='Cria um projeto'),
):
    result = subprocess.run(['poetry', 'new', '--flat', f'{name}'], check=True)

    if result.returncode == 0:
        secho('Projeto criado')
    else:
        secho('Erro ao criar projeto', fg=colors.RED)
