from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.crud.crud_user import CrudUser
from app.schemas.user import UserInfo

router = APIRouter()


@router.get("/user_info", response_model=UserInfo)
async def get_user_info(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = CrudUser.get_by_email(db=db, email=current_user)
    # data = UserInfo()
    return user
