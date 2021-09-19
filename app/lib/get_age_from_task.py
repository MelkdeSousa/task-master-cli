from typing import Literal, TypedDict, Union
from datetime import datetime

from app.lib import get_age

Task = TypedDict('Task', {
    'description': str,
    'status': Union[Literal['pending'], Literal['done']],
    'priority': Union[Literal['LOW'], Literal['NORMAL'], Literal['HIGH']],
    'created_at': str,
    'updated_at': str,
})


def get_age_from_task(task: Task):
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
