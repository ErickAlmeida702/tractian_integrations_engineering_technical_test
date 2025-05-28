import asyncio
import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from src.repositories.workorder_repository import TracOSWorkorderRepository
from src.services.inbound_service import InboundService
from src.services.outbound_service import OutboundService

logging.basicConfig(level=logging.INFO)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DATABASE", "tractian")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "workorders")
INBOUND_DIR = os.getenv("DATA_INBOUND_DIR", "../data/inbound")
OUTBOUND_DIR = os.getenv("DATA_OUTBOUND_DIR", "../data/outbound")


async def main() -> None:
    client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_URI)  # type: ignore[type-arg]
    db: AsyncIOMotorDatabase = client[MONGO_DB]  # type: ignore[type-arg]
    collection: AsyncIOMotorCollection = db[MONGO_COLLECTION]  # type: ignore[type-arg]

    repo = TracOSWorkorderRepository(collection)
    inbound = InboundService(repo, INBOUND_DIR)
    outbound = OutboundService(repo, OUTBOUND_DIR)

    await inbound.process_inbound_files()
    await outbound.export_unsynced_workorders()


if __name__ == "__main__":
    asyncio.run(main())
