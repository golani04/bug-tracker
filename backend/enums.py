from enum import StrEnum


class Status(StrEnum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"


class Priority(StrEnum):
    low = "low"
    normal = "normal"
    high = "high"
