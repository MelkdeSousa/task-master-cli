import click
from tabulate import tabulate
from datetime import datetime
from pysondb import db
import math


database = db.getDb('todo.db.json')


def template_time(days=0, hours=0, minutes=0):
    template_days = f'{days} days' if days > 0 else ""
    template_hours = f'{hours} hours' if hours > 0 else ""
    template_minutes = f'{" and " if template_hours  else ""}{minutes} minutes' if minutes > 0 else ""

    return f'{f"{template_days}, " if template_days else ""}{f"{template_hours}" if template_hours else ""}{template_minutes}'


def get_age(total_seconds: int):
    SECONDS_IN_MINUTES = 60
    SECONDS_IN_HOUR = 60 * 60
    SECONDS_IN_DAY = SECONDS_IN_HOUR * 24

    days = math.floor(total_seconds // SECONDS_IN_DAY)
    hours = math.floor((total_seconds - (days * SECONDS_IN_DAY)) // SECONDS_IN_HOUR)
    minutes = math.floor((total_seconds - (days * SECONDS_IN_DAY) - (hours * SECONDS_IN_HOUR)) // SECONDS_IN_MINUTES)

    return template_time(days, hours, minutes)


@click.command('add')
@click.argument('description')
@click.option('--priority', '-p', default='NORMAL', help='Priority task [LOW, NORMAL, HIGH]')
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


@click.command('complete', help='Mark task by ID with DONE')
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


@click.command('delete')
@click.argument('id')
def delete(id: int):
    database.deleteById(id)

    return True, 'Task deleted'


@click.command('list')
def list():
    tasks = database.getBy({'status': 'pending'})

    new_tasks = [
        {
            **task,
            'age': get_age((datetime.now() - datetime.fromisoformat(task['created_at'])).total_seconds())
        }
        for task in tasks
    ]

    click.echo(new_tasks)


@click.command('next')
def next(): pass


if __name__ == '__main__':
    list()
