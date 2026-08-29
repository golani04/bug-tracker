import json
from datetime import datetime, timedelta
from typing import Dict, Tuple

from fastapi import Depends, Request
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.config import settings
from backend.db import get_db
from backend.logger import logger
from backend.repositories.users import UserRepository
from backend.schemas.users import User as UserSchema
from backend.utils.exceptions import Unauthorized
from backend.utils.time import utcnow


class _Authorization:
    def __init__(self) -> None:
        self.auth_methods: Tuple[str, ...] = settings.AUTH_HEADERS
        self.cookie_name: str = settings.COOKIE_HEADER_NAME
        self.expiry_delta: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.algorithm: str = settings.ALGORITHM

    def _get_token(self, request: Request):
        if request is None:
            raise Unauthorized()

        token: str | None = None
        for method in self.auth_methods:
            if token:
                break

            match method:
                case "cookie":
                    token = request.cookies.get(self.cookie_name)
                case "headers":
                    _, token = get_authorization_scheme_param(request.headers.get("Authorization"))

        return token

    def _payload(self, token: str):
        try:
            if token is None:
                raise Unauthorized()

            decoded_token: Dict = jwt.decode(token, settings.SECRET_KEY, self.algorithm)
            return json.loads(decoded_token["sub"])
        except JWTError as error:
            logger.exception("Failed to decode an authorization token")
            raise Unauthorized() from error

    def create_access_token(self, claims: Dict, token_type: str = "access_type") -> str:
        now: datetime = utcnow()
        to_encode = {
            "type": token_type,
            "iat": now,
            "exp": now + timedelta(minutes=self.expiry_delta),
            "sub": json.dumps(claims),
        }

        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=self.algorithm)

    async def get_current_user(self, request: Request, session: Session = Depends(get_db)) -> UserSchema:
        payload: Dict = self._payload(self._get_token(request))

        user = UserRepository(session).get_by_id(payload["id"])
        if user is None:
            raise Unauthorized()

        return UserSchema.model_validate(user)


# auth_manager
auth_manager = _Authorization()
