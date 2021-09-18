from datetime import datetime
from .get_age import get_age


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
