import click
from tabulate import tabulate
from datetime import datetime
from pysondb import db
import math


database = db.getDb('todo.db.json')


def template_time(month=0, days=0, hours=0, minutes=0):
    template_month = f'{month} month(s)' if month > 0 else ""
    template_days = f'{days} days' if 0 < days < 30 else ""
    template_hours = f'{hours} hours' if hours > 0 else ""
    template_minutes = f'{" and " if template_hours  else ""}{minutes} minutes' if minutes > 0 else ""

    return f'{f"{template_month}, " if template_month else ""}{f"{template_days}, " if template_days else ""}{f"{template_hours}" if template_hours else ""}{template_minutes}'


def get_age(total_seconds: int):
    SECONDS_IN_MINUTES = 60
    SECONDS_IN_HOUR = 60 * 60
    SECONDS_IN_DAY = SECONDS_IN_HOUR * 24

    month = math.floor(total_seconds // SECONDS_IN_DAY * 30)

    days = math.floor(total_seconds // SECONDS_IN_DAY)
    hours = math.floor(
        (total_seconds - (days * SECONDS_IN_DAY)) // SECONDS_IN_HOUR)
    minutes = math.floor((total_seconds - (days * SECONDS_IN_DAY) -
                         (hours * SECONDS_IN_HOUR)) // SECONDS_IN_MINUTES)

    return template_time(month, days, hours, minutes)


@click.group()
def cli():
    pass


@cli.command('add')
@click.argument('description')
@click.option(
    '--priority', '-p',
    default='NORMAL',
    help='Priority task [LOW, NORMAL, HIGH]'
)
def add(description: str, priority: str):
    task = {
        'description': description,
        'status': 'pending',
        'priority': priority,
        'created_at': datetime.now().__str__(),
        'updated_at': datetime.now().__str__(),
    }

    database.add(task)

    return True, 'Task added successfully!'


@cli.command('complete', help='Mark task by ID with DONE')
@click.argument('id')
def complete(id: int):
    task = database.find(id)
    task_done = {
        **task,
        'status': 'done',
        'updated_at': datetime.now().__str__()
    }

    database.updateById(id, task_done)

    return True, 'Task completed successfully'


@cli.command('delete')
@click.argument('id')
def delete(id: int):
    database.deleteById(id)

    return True, 'Task deleted'


@cli.command('list', help='List tasks PENDING and DONE')
@click.option('-a', is_flag=True, help='List all tasks')
def list(a):
    if a:
        tasks = database.getAll()

        click.echo(tasks)

        return

    tasks = database.getBy({'status': 'pending'})

    tasks_with_age = [
        {
            **task,
            'age': get_age(
                (datetime.now() - datetime.fromisoformat(task['created_at']))
                .total_seconds()
            )
        }
        for task in tasks
    ]

    click.echo(tasks_with_age)

    return


@cli.command('next')
def next(): pass


if __name__ == '__main__':
    cli()
