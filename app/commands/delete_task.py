import click
from app.controllers import delete_task as delete_task_by_id

from app.lib import echo


@click.command('delete')
@click.argument('id')
def delete_task(id: int):
    """ Delete a task by id """

    try:
        task_deleted = delete_task_by_id(id)

        if not task_deleted:
            return echo('Task not deleted', 'red')

        return echo('Task deleted', 'green')
    except:
        return echo('Task not deleted', 'red')
