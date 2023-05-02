from datetime import datetime, timedelta, timezone
import json
import logging
from dataclasses import dataclass, field
from typing import Dict, Tuple

from fastapi import Depends, Request
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models.users import User
from backend.utils.exceptions import Unauthorized
from config import settings


logger = logging.getLogger("bug_tracker")


@dataclass
class _Authorization:
    auth_methods: Tuple[str] = field(default_factory=lambda: settings.AUTH_HEADERS)
    cookie_name: str = settings.COOKIE_HEADER_NAME
    expiry_delta: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    algorithm: str = settings.ALGORITHM

    def _get_token(self, request: Request):
        if request is None:
            raise Unauthorized()

        token: str | None = None
        for method in self.auth_methods:
            if token:
                return token

            if method == "cookie":
                token = request.cookies.get(self.cookie_name)

            elif method == "headers":
                _, token = get_authorization_scheme_param(request.headers.get("Authorization"))

        return token

    def _payload(self, token: str):
        try:
            if token is None:
                raise Unauthorized()

            decoded_token: Dict = jwt.decode(token, settings.SECRET_KEY, self.algorithm)
            return json.loads(decoded_token["sub"])
        except JWTError as e:
            logger.exception("Failed to decode an authorization token")
            raise Unauthorized() from e

    def create_access_token(self, claims: Dict, token_type: str = "access_type") -> str:
        now: datetime = datetime.now(timezone.utc)
        to_encode = {
            "type": token_type,
            "iat": now,
            "exp": now + timedelta(minutes=self.expiry_delta),
            "sub": json.dumps(claims),
        }

        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=self.algorithm)

    async def get_current_user(
        self, request: Request, sess: Session = Depends(get_db)
    ) -> User | None:
        payload: Dict = self._payload(self._get_token(request))

        return sess.query(User).filter_by(id=payload["id"]).first()


# auth_manager
auth_manager = _Authorization()
