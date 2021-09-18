from typing import Literal, TypedDict, Union
import click
from datetime import datetime
from tabulate import tabulate

from app.controllers import get_task
from app.lib import get_age, echo


Task = TypedDict('Task', {
    'description': str,
    'status': Union[Literal['pending'], Literal['done']],
    'priority': Union[Literal['LOW'], Literal['NORMAL'], Literal['HIGH']],
    'created_at': str,
    'updated_at': str,
})


def __get_age_from_task(task: Task):
    description, status, priority, created_at, _, id_task = task.values()

    return {
        'id': id_task,
        'description': description,
        'status': status,
        'priority': priority,
        'created_at': datetime.fromisoformat(created_at).strftime('%m/%d/%Y %H:%M'),
        'age': get_age(
            (datetime.now() - datetime.fromisoformat(task['created_at']))
            .total_seconds()
        )
    }


@click.command('list')
@click.option('-a', is_flag=True)
def list_tasks(a):
    r""" List all tasks """

    tasks = get_task({'status': 'pending'}) if not a else get_task()

    if not tasks:
        return echo('Not has task pending.', 'green')

    tasks_with_age = list(map(__get_age_from_task, tasks))

    return echo(tabulate(tasks_with_age, headers='keys',
                         tablefmt='fancy_grid', stralign='center', numalign='center'))
