from typing import Dict


class BugTrackerError(Exception):
    """Global project exception all custom errors should ingerit from."""

    def __init__(self, msg: Dict | str = "Unknown Error") -> None:
        super().__init__(msg if isinstance(msg, Dict) else {"messages": msg})


class AuthError(BugTrackerError):
    status_code: int = 400

    def __init__(self, msg: Dict | str = "Authentication Failed") -> None:
        super().__init__(msg)


class Unauthorized(AuthError):
    status_code: int = 401

    def __init__(self, msg: Dict | str = "Unauthorized") -> None:
        super().__init__(msg)


class Forbidden(AuthError):
    status_code: int = 403

    def __init__(self, msg: Dict | str = "Forbidden") -> None:
        super().__init__(msg)
