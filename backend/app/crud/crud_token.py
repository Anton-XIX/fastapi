from typing import Any, Dict, Optional, Union
from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.token import Token
from app.schemas.token import TokenCreate, TokenUpdate


class CRUDToken(CRUDBase[Token, TokenCreate, TokenUpdate]):
    def get_by_user_uuid(self, db: Session, *, user_uuid: UUID) -> Optional[Token]:
        return db.query(Token).filter(Token.user_uuid == user_uuid).first()

    def get_last_token_instance(self, db: Session, *, token: UUID) -> Optional[Token]:
        return (
            db.query(Token)
            .filter(Token.token == token)
            .order_by(Token.created_at.desc())
            .first()
        )


CrudToken = CRUDToken(Token)
