


from src.core.entities.task import Task


def from_sql_to_entity(model):
    print(type(model))
    return Task(
        title=model.title,
        description=model.description,
        uuid=model.uuid,
        created_at=model.created_at,
        updated_at=model.updated_at,
        is_completed=model.is_completed
    )