from typing import List, Literal, Tuple, TypedDict, Union
from pysondb import db

Task = TypedDict('Task', {
    'description': str,
    'status': Union[Literal['pending'], Literal['done']],
    'priority': Union[Literal['LOW'], Literal['NORMAL'], Literal['HIGH']],
    'created_at': str,
    'updated_at': str,
})


def get_task(query: dict = None):
    try:
        database = db.getDb('todo.db.json')

        if not query:
            return database.getAll()

        return database.getBy(query)
    except Exception as exception:
        raise exception
