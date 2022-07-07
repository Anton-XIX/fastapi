import datetime
import inspect
import os
from typing import Type

from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import ModelField


def to_snake_case(string: str) -> str:
    return "".join(["_" + i.lower() if i.isupper() else i for i in string]).lstrip("_")


def generate_directoty(model_name):
    directory = f"{model_name}/{str(datetime.datetime.now().date())}/"

    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def as_form(cls: Type[BaseModel]):
    """
    Allows use pydantic model as form.
    """
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField  # type: ignore

        new_parameters.append(
            inspect.Parameter(
                model_field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                default=Form(...)
                if not model_field.required
                else Form(model_field.default),
                annotation=model_field.outer_type_,
            )
        )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, "as_form", as_form_func)
    return cls
