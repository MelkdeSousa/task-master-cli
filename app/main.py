import click
from tabulate import tabulate
from datetime import datetime
from pysondb import db


database = db.getDb('todo.db.json')


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


@click.command('complete', help='Task ID')
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
def delete(): pass


@click.command('list')
def list(): pass


@click.command('next')
def next(): pass


if __name__ == '__main__':
    pass
