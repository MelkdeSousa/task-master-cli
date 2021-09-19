import click

from app.lib import get_age_from_task, tabulate, echo
from app.controllers import create_task, get_task


@click.command('add')
def add_task():
    r""" Create a task with priority and add to list of tasks """

    description = click.prompt('Description your task', type=str)
    priority = click.prompt(
        'Priority your task (LOW or HIGH)', type=str, default='NORMAL').upper()

    created = create_task(description, priority)
    tasks = list(map(get_age_from_task, get_task()))

    click.clear()

    if not created:
        return echo('Task not created.', 'red')

    echo(tabulate(tasks))
    return echo(f'Task "{created["description"]}" added', 'green')
