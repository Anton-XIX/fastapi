from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.auth.exceptions import IncorrectCredentialsException
from app.auth.services.write_token_to_db import WriteTokenToDb
from app.core.services.password_service import pass_service
from app.crud.crud_token import CrudToken
from app.crud.crud_user import CrudUser
from app.models.choices import TokenType
from app.schemas.token import RenewToken
from app.schemas.user import UserLogin

router = APIRouter()


@router.post("/login")
def login(
    request: Request,
    user: UserLogin,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    request_user = CrudUser.get_by_email(db=db, email=user.email)
    verify_password = pass_service.verify_password(
        password=user.password, salt=request_user.salt, hashed_pw=request_user.password
    )
    if not (request_user and verify_password):
        raise IncorrectCredentialsException(
            status_code=status.HTTP_400_BAD_REQUEST,
            mesaage="Incorrect login or password",
        )
    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    token_data = {
        TokenType.access.value: access_token,
        TokenType.refresh.value: refresh_token,
    }
    save_tokens_service = WriteTokenToDb(
        token_data=token_data, user_uuid=request_user.uuid, db=db
    )
    save_tokens_service.perform()
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/user_info")
def get_user_info(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@router.post("/refresh")
def refresh(
    token_data: RenewToken = None,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    if not token_data:
        Authorize.jwt_refresh_token_required()
        current_user_email = Authorize.get_jwt_subject()
        current_user = CrudUser.get_by_email(email=current_user_email, db=db)
    else:
        token = CrudToken.get_last_token_instance(token=token_data.refresh_token, db=db)
        current_user = CrudUser.get_by_uuid(uuid=token.user_uuid, db=db)
    new_access_token = Authorize.create_access_token(subject=current_user.email)
    token_data = {TokenType.access.value: new_access_token}
    save_tokens_service = WriteTokenToDb(
        token_data=token_data, user_uuid=current_user.uuid, db=db
    )
    save_tokens_service.perform()
    return {"access_token": new_access_token}
