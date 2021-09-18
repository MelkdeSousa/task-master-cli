from pysondb import db


def delete_task(task_id: int):
    try:
        database = db.getDb('todo.db.json')

        return database.deleteById(task_id)
    except Exception as exception:
        raise exception
