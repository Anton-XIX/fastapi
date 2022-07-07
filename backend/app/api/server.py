from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException, MissingTokenError

from app.api.routers import router as api_router
from app.auth.config import auth_config
from app.core import config, tasks
from app.core.exceptions import (
    IncorrectCredentialsException,
    IncorrectFormData,
    NotFound,
    UserAlreadyExists,
    UserNotFound,
)

# AuthJWT.load_config(AuthSettings)


@AuthJWT.load_config
def get_config():
    return auth_config


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in denylist


def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_event_handler("startup", tasks.create_start_app_handler())

    app.include_router(api_router, prefix="/api")

    return app


app = get_application()

denylist = set()


# ---------------------- Exceptions ------------------------------- #


@app.exception_handler(AuthJWTException)
async def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    """ "
    Add logging??
    """
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(MissingTokenError)
async def no_token_exception_handler(request: Request, exc: MissingTokenError):
    """ "
    Add logging??
    """
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(IncorrectCredentialsException)
async def incorrect_credentials_exception_handler(
    request: Request, exc: IncorrectCredentialsException
):
    """ "
    Add logging??
    """
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(UserNotFound)
async def user_not_fount_exception_handler(request: Request, exc: UserNotFound):
    """ "
    Add logging??
    """
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(UserAlreadyExists)
async def user_not_fount_exception_handler(request: Request, exc: UserAlreadyExists):
    """ "
    Add logging??
    """
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(IncorrectFormData)
async def user_not_fount_exception_handler(request: Request, exc: UserAlreadyExists):
    """ "
    Add logging??
    """
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Rework
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors()[0]["msg"]}),
    )


@app.exception_handler(NotFound)
async def validation_exception_handler(request: Request, exc: NotFound):
    # Rework
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({"detail": exc.message}),
    )
