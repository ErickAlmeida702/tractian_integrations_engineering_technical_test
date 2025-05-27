import asyncio
import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from src.repositories.workorder_repository import TracOSWorkorderRepository
from src.services.inbound_service import InboundService
from src.services.outbound_service import OutboundService

logging.basicConfig(level=logging.INFO)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DATABASE", "tractian")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "workorders")
INBOUND_DIR = os.getenv("DATA_INBOUND_DIR", "../data/inbound")
OUTBOUND_DIR = os.getenv("DATA_OUTBOUND_DIR", "../data/outbound")


async def main():
    client = AsyncIOMotorClient(MONGO_URI)
    collection = client[MONGO_DB][MONGO_COLLECTION]

    repo = TracOSWorkorderRepository(collection)
    inbound = InboundService(repo, INBOUND_DIR)
    outbound = OutboundService(repo, OUTBOUND_DIR)

    await inbound.process_inbound_files()
    await outbound.export_unsynced_workorders()


if __name__ == "__main__":
    asyncio.run(main())
