import logging

from sqlalchemy.orm import Session

from core.services.password_service import pass_service
from crud import CrudUser, CRUDUserProfile
from db import base  # noqa: F401
from schemas.user import UserCreate
from schemas.user_profile import UserProfileCreate
logger = logging.getLogger(__name__)


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    email = "a.kiryakou@mail.ru"
    user = CrudUser.get_by_email(db, email=email)
    password = "qwerty"
    salt = pass_service.generate_salt()
    hashed_password = pass_service.hash_password(password=password, salt=salt)
    if not user:
        user_in = UserCreate(
            email=email,
            is_superuser=True,
            password=hashed_password,
            salt=salt,
        )
        user = CrudUser.create(db=db, obj_in=user_in)
        user_profile = UserProfileCreate(
            first_name='Anton',
        last_name = 'Kiryakou',
        birth_date = None,
        user_uuid = user.uuid)
        user_profile = CRUDUserProfile.create(db=db, obj_in=user_profile)
    else:
        logger.info(
            "Skipping creating superuser. User with email " f"{email} already exists. "
        )
