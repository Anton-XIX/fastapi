from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.token import Token
from app.schemas.token import TokenCreate, TokenUpdate


class CRUDToken(CRUDBase[Token, TokenCreate, TokenUpdate]):
    def get_by_user_uuid(self, db: Session, *, user_uuid: UUID) -> Optional[Token]:
        return db.query(Token).filter(Token.user_uuid == user_uuid).first()

    def get_token_instance_by_token(
        self, db: Session, *, token: str
    ) -> Optional[Token]:
        return db.query(Token).filter(Token.token == token).first()

    def disable_token(self, db: Session, *, token: str) -> None:
        token = self.get_token_instance_by_token(db=db, token=token)
        updated_token = TokenUpdate(fresh=False)
        CrudToken.update(db=db, db_obj=token, obj_in=updated_token)


CrudToken = CRUDToken(Token)
