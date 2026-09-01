import base64
import hashlib

import bcrypt


def _prehash(passw: str) -> bytes:
    # bcrypt only reads the first 72 bytes of its input and truncates at a NUL byte,
    # so passwords are SHA-256 hashed and base64-encoded before bcrypt sees them.
    digest = hashlib.sha256(passw.encode("utf-8")).digest()
    return base64.b64encode(digest)


def hash_password(passw: str) -> str:
    return bcrypt.hashpw(_prehash(passw), bcrypt.gensalt()).decode("utf-8")


def verify_password(passw: str, hashed: bytes | str) -> bool:
    hashed_bytes = hashed.encode("utf-8") if isinstance(hashed, str) else hashed
    return bcrypt.checkpw(_prehash(passw), hashed_bytes)
