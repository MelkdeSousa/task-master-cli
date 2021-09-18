from stringcolor import cs
import click


def echo(text: str, color='white', bg=None):
    return click.echo(cs(text, color, bg))
