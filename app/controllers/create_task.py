from datetime import datetime
from typing import Literal, Tuple, TypedDict, Union
from pysondb import db


Task = TypedDict('Task', {
    'description': str,
    'status': Union[Literal['pending'], Literal['done']],
    'priority': Union[Literal['LOW'], Literal['NORMAL'], Literal['HIGH']],
    'created_at': str,
    'updated_at': str,
})


def create_task(description: str, priority: str):
    database = db.getDb('todo.db.json')

    task: Task = {
        'description': description,
        'status': 'pending',
        'priority': priority,
        'created_at': datetime.now().__str__(),
        'updated_at': datetime.now().__str__(),
    }

    task_created = database.add(task)

    if not task_created:
        return

    return task
