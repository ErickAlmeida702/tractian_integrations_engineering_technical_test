from typing import Optional, Literal
from pydantic import BaseModel
from datetime import datetime


class CustomerWorkorder(BaseModel):
    orderNo: int
    isCanceled: bool
    isDeleted: bool
    isDone: bool
    isOnHold: bool
    isPending: bool
    summary: str
    creationDate: datetime
    lastUpdateDate: datetime
    deletedDate: Optional[datetime] = None


class TracOSWorkorder(BaseModel):
    number: int
    status: Literal["pending", "in_progress", "completed", "on_hold", "cancelled"]
    title: str
    description: str
    createdAt: datetime
    updatedAt: datetime
    deleted: bool
    deletedAt: Optional[datetime] = None
    isSynced: Optional[bool] = False
    syncedAt: Optional[datetime] = None
