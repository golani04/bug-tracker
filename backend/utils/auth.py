from passlib.hash import bcrypt_sha256


def hash_password(passw: str) -> str:
    return bcrypt_sha256.hash(passw)


def verify_password(passw: str, hashed: str) -> bool:
    return bcrypt_sha256.verify(passw, hashed)
