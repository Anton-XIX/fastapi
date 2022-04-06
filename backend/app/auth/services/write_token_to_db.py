from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.crud.crud_token import CrudToken
from app.crud.crud_user import CrudUser
from app.schemas.token import TokenCreate


class WriteTokenToDb:
    def __init__(self, token_data: dict, user_uuid: UUID, db: Session) -> None:
        self.token_data = token_data
        self.user_uuid = user_uuid
        self.db = db

    def perform(self) -> bool:
        if self._validate_user_uuid():
            pass
        for token_type, token in self.token_data.items():
            token = TokenCreate(
                token_type=token_type, token=token, user_uuid=self.user_uuid
            )
            CrudToken.create(db=self.db, obj_in=token)
        return True

    def _validate_user_uuid(self) -> bool:
        user = CrudUser.get_by_uuid(uuid=self.user_uuid, db=self.db)
        if user:
            return True
        return False
