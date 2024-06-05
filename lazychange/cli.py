import click

from .commands.bump import bump

@click.group()
def cli() -> None:
    pass

cli.add_command(bump)

if __name__ == "__main__":
    cli()
