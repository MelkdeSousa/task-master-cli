from typing import Any, Dict, Literal, Tuple, TypedDict, Union
from pysondb import db


Task = TypedDict('Task', {
    'description': str,
    'status': Union[Literal['pending'], Literal['done']],
    'priority': Union[Literal['LOW'], Literal['NORMAL'], Literal['HIGH']],
    'created_at': str,
    'updated_at': str,
})


def update_task(task_id: Union[str, int], **fields: Dict[str, Any]):
    database = db.getDb('todo.db.json')

    task = database.find(task_id)

    updated_task = {**task, **fields}

    database.updateById(task_id, updated_task)

    return updated_task
