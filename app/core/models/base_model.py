from typing import Dict, Any

import orjson
from pydantic import BaseModel as PydanticBaseModel, Extra


def _orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseModel(PydanticBaseModel):
    """
    Base model for all API schemas.
    """
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        extra = Extra.ignore
        json_loads = orjson.loads
        json_dumps = orjson.dumps


def model_to_jsonable_dict(model: BaseModel, **kwargs) -> Dict[str, Any]:
    return orjson.loads(model.json(**kwargs))
