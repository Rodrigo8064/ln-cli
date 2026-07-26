from typing import Annotated

from rich.console import Console
from typer import Context, Exit, Option, Typer

from ln_cli import __version__
from ln_cli.commands import docker, install, linux_tips, new_project

console = Console()
app = Typer()


def version_callback(value: bool):
    if value:
        print(__version__)
        raise Exit(code=0)


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    version: Annotated[
        bool | None, Option('--version', callback=version_callback)
    ] = None,
):
    message = """Como utilizar"""
    if ctx.invoked_subcommand:
        return
    console.print(message)


app.add_typer(new_project.app, name='new')
app.add_typer(install.app, name='install')
app.add_typer(docker.app, name='docker')
app.add_typer(linux_tips.app, name='linux-tips')
