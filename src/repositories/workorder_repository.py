from typing import Any, Optional, cast

from motor.motor_asyncio import AsyncIOMotorCollection
from src.domain.models import TracOSWorkorder
from datetime import datetime
from pymongo import ReturnDocument
from src.domain.types import TracOSWorkorderDict



class TracOSWorkorderRepository:
    def __init__(self, collection: AsyncIOMotorCollection[Any]):
        self.collection = collection

    async def upsert(self, workorder: TracOSWorkorder) -> Optional[TracOSWorkorderDict]:
        result = await self.collection.find_one_and_update(
            {"number": workorder.number},
            {"$set": workorder.model_dump()},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return cast(Optional[TracOSWorkorderDict], result)

    async def get_unsynced(self) -> list[TracOSWorkorderDict]:
        cursor = self.collection.find({"isSynced": False})
        return await cursor.to_list(length=None)

    async def mark_as_synced(self, number: int) -> None:
        await self.collection.update_one(
            {"number": number},
            {
                "$set": {
                    "isSynced": True,
                    "syncedAt": datetime.utcnow(),
                }
            }
        )
