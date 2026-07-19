from rich.console import Console
from typer import Context, Exit, Option, Typer

from ln_cli import __version__
from ln_cli.commands import new_project

console = Console()
app = Typer()


def version(flag):
    if flag:
        print(__version__)
        raise Exit(code=0)


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    version: bool = Option(False, callback=version, is_flag=True),
):
    message = """Como utilizar"""
    if ctx.invoked_subcommand:
        return
    console.print(message)


app.add_typer(new_project.app, name='project')
