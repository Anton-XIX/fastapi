from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.figures import MultiLineFigure
from app.schemas.figures import MultiLineFigureCreate, MultiLineFigureUpdate


class CRUDMultiLineFigure(
    CRUDBase[MultiLineFigure, MultiLineFigureCreate, MultiLineFigureUpdate]
):
    def update(
        self,
        db: Session,
        *,
        db_obj: MultiLineFigure,
        obj_in: Union[MultiLineFigureUpdate, Dict[str, Any]]
    ) -> MultiLineFigure:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


CrudMultiLineFigure = CRUDMultiLineFigure(MultiLineFigure)
