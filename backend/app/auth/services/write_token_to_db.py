import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.auth.config import auth_config
from app.core.exceptions import UserNotFound
from app.crud.crud_token import CrudToken
from app.crud.crud_user import CrudUser
from app.models.choices import TokenType
from app.schemas.token import TokenCreate


class WriteTokenToDb:
    expiration = {
        TokenType.access.value: auth_config.authjwt_access_token_expires,
        TokenType.refresh.value: auth_config.authjwt_refresh_token_expires,
    }

    def __init__(self, token_data: dict, user_uuid: UUID, db: Session) -> None:
        self.token_data = token_data
        self.user_uuid = user_uuid
        self.db = db

    def perform(self) -> bool:
        self._validate_user_uuid()
        for token_type, token in self.token_data.items():
            token = TokenCreate(
                token_type=token_type,
                token=token,
                user_uuid=self.user_uuid,
                expiration_date=datetime.datetime.now()
                + datetime.timedelta(seconds=self.expiration.get(token_type)),
            )
            CrudToken.create(db=self.db, obj_in=token)
        return True

    def _validate_user_uuid(self):
        user = CrudUser.get_by_uuid(uuid=self.user_uuid, db=self.db)
        if not user:
            raise UserNotFound(message="User not found.")
