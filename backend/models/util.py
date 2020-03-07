from hashlib import sha256
from typing import NewType

ItemID = NewType("ItemID", sha256)
