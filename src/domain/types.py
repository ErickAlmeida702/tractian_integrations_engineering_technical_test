from typing import TypedDict, Literal, Optional
from datetime import datetime

class TracOSWorkorderDict(TypedDict, total=False):
    number: int
    title: str
    status: Literal["pending", "in_progress", "completed", "on_hold", "cancelled"]
    createdAt: datetime
    updatedAt: datetime
    deleted: bool
    deletedAt: Optional[datetime]
    isSynced: bool
    syncedAt: Optional[datetime]