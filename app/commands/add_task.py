import click

from app.lib import echo
from app.controllers import create_task


@click.command('add')
@click.argument('description')
@click.option(
    '--priority', '-p',
    help='Priority task [LOW, NORMAL, HIGH]',
    default='NORMAL'
)
def add_task(description: str, priority: str):
    r""" Create a task with priority and add to list of tasks """

    created = create_task(description, priority)

    if not created:
        echo('Task not created.', 'red')

    return echo(f'Task "{created["description"]}" added', 'green')
