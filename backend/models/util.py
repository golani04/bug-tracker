import secrets


def create_id():
    return secrets.token_hex()
