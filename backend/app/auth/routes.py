from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.auth.services.write_token_to_db import WriteTokenToDb
from app.core.exceptions import IncorrectCredentialsException, UserNotFound
from app.core.services.create_user_service import CreateUserService
from app.core.services.password_service import pass_service
from app.crud.crud_token import CrudToken
from app.crud.crud_user import CrudUser
from app.models.choices import TokenType
from app.schemas.token import RenewToken
from app.schemas.user import UserLogin, UserRegister

router = APIRouter()


@router.post("/login")
async def login(
    user: UserLogin,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    request_user = CrudUser.get_by_email(db=db, email=user.email)
    if request_user:
        verify_password = pass_service.verify_password(
            password=user.password,
            salt=request_user.salt,
            hashed_pw=request_user.password,
        )
        if not verify_password:
            raise IncorrectCredentialsException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Incorrect credentials",
            )
    else:
        raise UserNotFound(
            message="Incorrect credentials",
        )

    access_token = Authorize.create_access_token(
        subject=user.email,
    )
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    token_data = {
        TokenType.access.value: access_token,
        TokenType.refresh.value: refresh_token,
    }
    save_tokens_service = WriteTokenToDb(
        token_data=token_data, user_uuid=request_user.uuid, db=db
    )
    save_tokens_service.perform()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "user": user.email,
        },
    )


@router.post("/logout")
async def logout(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    CrudToken.disable_token(db=db, token=Authorize._token)
    return JSONResponse(status_code=status.HTTP_200_OK)


@router.post("/refresh")
async def refresh(
    token_data: RenewToken = None,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    if not token_data:
        Authorize.jwt_refresh_token_required()
        current_user_email = Authorize.get_jwt_subject()
        current_user = CrudUser.get_by_email(email=current_user_email, db=db)
    else:
        token = CrudToken.get_token_instance_by_token(
            token=token_data.refresh_token, db=db
        )
        current_user = CrudUser.get_by_uuid(uuid=token.user_uuid, db=db)
    new_access_token = Authorize.create_access_token(subject=current_user.email)
    token_data = {TokenType.access.value: new_access_token}
    save_tokens_service = WriteTokenToDb(
        token_data=token_data, user_uuid=current_user.uuid, db=db
    )
    save_tokens_service.perform()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"accessToken": new_access_token}
    )


@router.post("/register")
async def register(
    user: UserRegister = None,
    db: Session = Depends(get_db),
):
    # if not user:
    #     pass
    # if not (user.email and user.password):
    #     raise IncorrectFormData(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         message="Incorrect data",
    #     )
    user_create_service = CreateUserService(user_data=user, db=db)
    user_create_service.perform()
    return JSONResponse(status_code=status.HTTP_201_CREATED)
