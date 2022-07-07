from sqlalchemy.orm import Session

from app.core.exceptions import UserAlreadyExists
from app.core.services.password_service import pass_service
from app.crud.crud_user import CrudUser
from app.crud.crud_user_profile import CRUDUserProfile
from app.schemas.user import UserCreate, UserRegister
from app.schemas.user_profile import UserProfileCreate


class CreateUserService:
    def __init__(self, user_data: UserRegister, db: Session) -> None:
        self.user_data = user_data.dict()
        self.db = db

    def perform(self) -> bool:
        email = self.user_data["email"]
        self._validate_user_email(email)
        salt = pass_service.generate_salt()
        hashed_password = pass_service.hash_password(
            password=self.user_data["password"], salt=salt
        )
        self.user_data["password"] = hashed_password
        user_create_data = UserCreate(**self.user_data, salt=salt)
        user = CrudUser.create(db=self.db, obj_in=user_create_data)
        user_profile = UserProfileCreate(
            user_uuid=user.uuid,
            **self.user_data["user_profile"],
        )
        CRUDUserProfile.create(db=self.db, obj_in=user_profile)
        return True

    def _validate_user_email(self, user_email):
        user = CrudUser.get_by_email(email=user_email, db=self.db)
        if user:
            raise UserAlreadyExists(
                message=f"User with email {user_email} already exists."
            )
