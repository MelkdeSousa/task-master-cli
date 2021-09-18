from pyfiglet import Figlet
import click

from app.commands import (
    add_task,
    complete_task,
    list_tasks,
    delete_task,
    list_next_tasks
)


@click.group()
def cli(): pass


cli.add_command(add_task)
cli.add_command(complete_task)
cli.add_command(delete_task)
cli.add_command(list_tasks)
cli.add_command(list_next_tasks)

if __name__ == '__main__':
    cli()
