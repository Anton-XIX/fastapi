from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import UserProfile
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate


class CRUDUserProfile(CRUDBase[UserProfile, UserProfileCreate, UserProfileUpdate]):
    def get_by_user__uuid(
        self, db: Session, *, user_uuid: str
    ) -> Optional[UserProfile]:
        return db.query(UserProfile).filter(UserProfile.user_uuid == user_uuid).first()

    def update(
        self,
        db: Session,
        *,
        db_obj: UserProfile,
        obj_in: Union[UserProfileUpdate, Dict[str, Any]]
    ) -> UserProfile:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


CRUDUserProfile = CRUDUserProfile(UserProfile)
