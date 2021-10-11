from typing import Any
from fastapi.encoders import jsonable_encoder


def obj_in_to_db_obj(model: Any, obj_in: Any):
    obj_in_data = jsonable_encoder(obj_in)
    return model(**obj_in_data)

def obj_in_to_db_obj_attrs(obj_in: Any, db_obj: Any):
    obj_data = jsonable_encoder(db_obj)
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])

    return db_obj
