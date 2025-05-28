import json
import tempfile
import asyncio
import mongomock
import pytest
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from src.repositories.workorder_repository import TracOSWorkorderRepository
from src.services.inbound_service import InboundService
from src.services.outbound_service import OutboundService

sample_workorder = {
    "orderNo": 1,
    "isCanceled": False,
    "isDeleted": False,
    "isDone": True,
    "isOnHold": False,
    "isPending": False,
    "summary": "Trocar correia",
    "creationDate": "2024-10-10T10:00:00Z",
    "lastUpdateDate": "2024-10-12T10:00:00Z"
}

@pytest.mark.asyncio
async def test_end_to_end_flow():
    with tempfile.TemporaryDirectory() as inbound_dir, tempfile.TemporaryDirectory() as outbound_dir:

        input_path = Path(inbound_dir) / "workorder_1.json"

        with open(input_path, "w") as f:
            json.dump(sample_workorder, f)

        mock_client = mongomock.MongoClient()
        motor_client = AsyncIOMotorClient()
        motor_client.get_io_loop = asyncio.get_running_loop
        motor_client._topology = mock_client._topology

        collection = motor_client["tractian"]["workorders"]
        repo = TracOSWorkorderRepository(collection)

        inbound_service = InboundService(repo, inbound_dir)
        await inbound_service.process_inbound_files()

        outbound_service = OutboundService(repo, outbound_dir)
        await outbound_service.export_unsynced_workorders()

        exported_files = list(Path(outbound_dir).glob("*.json"))
        assert len(exported_files) == 1

        with open(exported_files[0], "r") as f:
            exported_data = json.load(f)
            assert exported_data["orderNo"] == 1
            assert exported_data["summary"] == "Trocar correia"

