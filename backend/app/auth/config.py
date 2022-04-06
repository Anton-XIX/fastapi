from pydantic import BaseModel

from app.core.config import SECRET_KEY, TOKEN_DENY_LIST


class AuthSettings(BaseModel):
    authjwt_secret_key: str = str(SECRET_KEY)
    # authjwt_denylist_enabled: bool = TOKEN_DENY_LIST
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
