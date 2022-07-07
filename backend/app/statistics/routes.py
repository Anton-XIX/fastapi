from typing import List

from fastapi import APIRouter, Depends, File, Path, UploadFile
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.core.exceptions import IncorrectFormData, NotFound
from app.crud.crud_user import CrudUser
from app.models.figures import MultiLineFigure
from app.schemas.figures import MultiLineFigureGet, MultiLineFigurePost
from app.statistics.services.create_multiline_figure import CreateMultiLineFigure

router = APIRouter()


@router.post("/multiline", response_model=MultiLineFigureGet)
async def create_multiline(
    figure: MultiLineFigurePost = Depends(MultiLineFigurePost.as_form),
    file: UploadFile = File(
        ...,
    ),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    if file.content_type not in ["text/csv"]:
        raise IncorrectFormData(
            400, "Invalid file type. Only .csv files allowed for uploading"
        )
    current_user = Authorize.get_jwt_subject()
    user = CrudUser.get_by_email(db=db, email=current_user)
    service = CreateMultiLineFigure(
        figure.dict(), file=file.file, user_uuid=user.uuid, db=db
    )
    service.perform()
    return service.instance


@router.post("/multiline/preview", response_model=MultiLineFigureGet)
async def create_multiline(
    figure: MultiLineFigurePost = Depends(MultiLineFigurePost.as_form),
    file: UploadFile = File(
        ...,
    ),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    if file.content_type not in ["text/csv"]:
        raise IncorrectFormData(
            400, "Invalid file type. Only .csv files allowed for uploading"
        )
    current_user = Authorize.get_jwt_subject()
    user = CrudUser.get_by_email(db=db, email=current_user)
    from statistics.services.create_multiline_figure import PrebuildMultiLineFigure

    service = PrebuildMultiLineFigure(
        figure.dict(), file=file.file, user_uuid=user.uuid, db=db
    )
    service.perform()
    return service.instance


@router.get("/charts", response_model=List[MultiLineFigureGet])
async def get_charts_list(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = CrudUser.get_by_email(db=db, email=current_user)
    return list(user.figures)


@router.get("/charts/{item_id}", response_model=MultiLineFigureGet)
async def get_chart(
    item_id: int = Path(..., title="The ID of the item to get"),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = CrudUser.get_by_email(db=db, email=current_user)
    figure = user.figures.filter(MultiLineFigure.id == item_id).one_or_none()
    if not figure:
        raise NotFound(404, f"Chart with id={item_id} doesn't exists")
    return figure
