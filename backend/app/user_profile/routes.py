from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.crud.crud_user import CrudUser
from app.crud.crud_user_profile import CRUDUserProfile
from app.schemas.user_profile import UserProfileUpdate

router = APIRouter()


@router.put("/user_profile", response_model=UserProfileUpdate)
async def user_profile(
    user_profile: UserProfileUpdate,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = CrudUser.get_by_email(db=db, email=current_user)
    profile = CRUDUserProfile.update(db=db, db_obj=user.profile, obj_in=user_profile)
    return profile


# @router.post('/upload-photo')
# async def upload_photo(file: UploadFile or None = None,
#                        Authorize: AuthJWT = Depends(),
#                        db: Session = Depends(get_db),
#                        ):
#     Authorize.jwt_required()
#     current_user = Authorize.get_jwt_subject()
#     user = CrudUser.get_by_email(db=db, email=current_user)
#     file_directoty = generate_directoty('user_profile')
#     with open(file_directoty+file.filename, "wb+") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     # import os
#     # file_path = os.path.join(file_directoty, file.filename)
#     # if os.path.exists(file_path):
#     #     return FileResponse(file_path, media_type="image/jpeg+svg", filename='test')
#     return {'1':'2'}
