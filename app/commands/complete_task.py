from datetime import datetime
import click

from app.lib import echo
from app.controllers import update_task


@click.command('complete')
@click.argument('id')
def complete_task(id: int):
    """ Mark task as completed by id """

    now = datetime.now().__str__()

    updated_task = update_task(id, status='done', updated_at=now)

    if updated_task:
        return echo('Task completed successfully', 'green')

    echo('Task not completed because not exists', 'red')
