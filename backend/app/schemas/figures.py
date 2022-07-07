from typing import Any, List
from uuid import UUID

from fastapi_camelcase import CamelModel
from pydantic import Field

from app.core.utils import as_form
from app.models.figures import MultiLineFigure


class FigureBase(CamelModel):
    name: str
    description: str
    figure_type: str = Field(default="multiline")
    public: bool = False


@as_form
class MultiLineFigurePost(FigureBase):
    ...
    x_axis_column: int
    y_axis_columns: Any

    class Config:
        orm_mode = True
        orig_model = MultiLineFigure


class MultiLineFigureCreate(FigureBase):
    user_uuid: UUID
    description: str
    x_axis: list
    datasets: dict


class MultiLineFigureUpdate(MultiLineFigureCreate):
    ...


class MultiLineFigureGet(FigureBase):
    id: int = None
    x_axis: list
    datasets: dict
    description: Any
    ...

    class Config:
        orm_mode = True
        orig_model = MultiLineFigure


class FigureList(CamelModel):
    figures: List[MultiLineFigureGet]
