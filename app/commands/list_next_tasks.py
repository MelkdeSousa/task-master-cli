from datetime import datetime
from functools import reduce
import click
from pysondb import db
from tabulate import tabulate
from stringcolor import cs

from app.lib import get_oldest_tasks
from app.controllers import get_task


def make_task(fields):
    if not fields:
        return

    task = dict(reduce(lambda accumulator, current: {
        **accumulator, current: fields[current]}, fields, dict()))

    priority = task['priority']
    status = task['status']
    created_at = datetime.fromisoformat(
        task['created_at']).strftime('%m/%d/%Y %H:%M')

    pending_color = 'red' if status == 'pending' else 'green'
    priority_color = ('#62ff96' if priority == 'LOW'
                      else ('#ff6262' if priority == 'HIGH' else '#ff9962'))

    task_decorated = {
        **task,
        'created_at': created_at,
        'status': cs(status, pending_color),
        'priority': cs(priority, priority_color)
    }

    task_decorated.pop('updated_at')

    return task_decorated


@click.command('next')
def list_next_tasks():
    """ List the next tasks that must be completed """

    low_tasks = get_task({'priority': 'LOW'})
    normal_tasks = get_task({'priority': 'NORMAL'})
    high_tasks = get_task({'priority': 'HIGH'})

    old_low_task = get_oldest_tasks(low_tasks)
    old_normal_task = make_task(get_oldest_tasks(normal_tasks))
    old_high_task = get_oldest_tasks(high_tasks)

    tasks = [old_normal_task, ]

    click.echo(tabulate(tasks, headers='keys', tablefmt="fancy_grid",
               stralign="center", numalign="center"))
