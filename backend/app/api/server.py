from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException, MissingTokenError

from app.api.routers import router as api_router
from app.auth.config import AuthSettings
from app.auth.exceptions import IncorrectCredentialsException
from app.core import config, tasks

# AuthJWT.load_config(AuthSettings)


@AuthJWT.load_config
def get_config():
    return AuthSettings()


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
