import click
from tabulate import tabulate
from datetime import datetime
from pysondb import db
import math
from functools import reduce
from stringcolor import cs


database = db.getDb('todo.db.json')


def template_time(month=0, days=0, hours=0, minutes=0):
    template_month = f'{month} months' if month > 1 else f'{month} month' if 0 < month <= 1 else ""
    template_days = f'{days} days' if 0 < days < 30 else ""
    template_hours = f'{hours} hours' if hours > 0 else ""
    template_minutes = f'{" and " if template_hours  else ""}{minutes} minutes' if minutes > 0 else ""

    final_template = [
        f"{template_month}, " if template_month else "",
        f"{template_days}, " if template_days else "",
        f"{template_hours}" if template_hours else "",
        template_minutes
    ]

    return reduce(lambda prev, curr: f'{prev}{curr}', final_template, '')


def get_age(total_seconds: int):
    SECONDS_IN_MINUTES = 60
    SECONDS_IN_HOUR = 60 * 60
    SECONDS_IN_DAY = SECONDS_IN_HOUR * 24

    days = math.floor(total_seconds // SECONDS_IN_DAY)

    month = days // 30

    hours = math.floor(
        (total_seconds - (days * SECONDS_IN_DAY)) // SECONDS_IN_HOUR)
    minutes = math.floor((total_seconds - (days * SECONDS_IN_DAY) -
                         (hours * SECONDS_IN_HOUR)) // SECONDS_IN_MINUTES)

    return template_time(month, days, hours, minutes)


def get_oldest_tasks(tasks: list):
    if not len(tasks):
        return

    dates_tasks = [
        datetime.fromisoformat(task['created_at'])
        for task in tasks
    ]

    oldest_task = min(dates_tasks)

    task, = [
        {
            **task,
            'age': get_age(
                (datetime.now() - datetime.fromisoformat(task['created_at']))
                .total_seconds()
            )
        }
        for task in tasks if datetime.fromisoformat(
            task['created_at']) == oldest_task
    ]

    return task


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
def list_next_tasks():
    low_tasks = database.getBy({'priority': 'LOW'})
    normal_tasks = database.getBy({'priority': 'NORMAL'})
    high_tasks = database.getBy({'priority': 'HIGH'})

    old_low_task = get_oldest_tasks(low_tasks)
    old_normal_task = get_oldest_tasks(normal_tasks)
    old_high_task = get_oldest_tasks(high_tasks)

    tasks = [
        {
            'id': old_high_task['id'],
            'description': old_high_task['description'],
            'status': cs(old_high_task['status'], 'green') if old_high_task['status'] == 'done' else old_high_task['status'],
            'priority': cs(old_high_task['priority'], 'red'),
            'age': old_high_task['age']
        },
        {
            'id': old_normal_task['id'],
            'description': old_normal_task['description'],
            'status': cs(old_normal_task['status'], 'green') if old_normal_task['status'] == 'done' else old_normal_task['status'],
            'priority': cs(old_normal_task['priority'], 'yellow'),
            'age': old_normal_task['age']
        },
        {
            'id': old_low_task['id'],
            'description': old_low_task['description'],
            'status': cs(old_low_task['status'], 'green') if old_low_task['status'] == 'done' else old_low_task['status'],
            'priority': cs(old_low_task['priority'], 'cyan'),
            'age': old_low_task['age']
        }]

    click.echo(tabulate(tasks, headers='keys', tablefmt="fancy_grid"))


if __name__ == '__main__':
    cli()
